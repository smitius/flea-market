import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from PIL import Image, ImageOps
from app import db
from app.models import Item, ItemImage, SiteSettings, UserSession, FailedLoginAttempt

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
def dashboard():
    sort_by = request.args.get('sort', 'created_at')
    
    if sort_by == 'views':
        items = Item.query.order_by(Item.view_count.desc()).all()
    elif sort_by == 'name':
        items = Item.query.order_by(Item.name.asc()).all()
    elif sort_by == 'price':
        items = Item.query.order_by(Item.price.desc()).all()
    else:  # default to created_at
        items = Item.query.order_by(Item.created_at.desc()).all()
    
    # Get active sessions for current user
    active_sessions = UserSession.query.filter_by(
        user_id=current_user.id,
        is_active=True
    ).order_by(UserSession.last_activity.desc()).all()
    
    # Clean up expired sessions and old failed attempts
    UserSession.cleanup_expired_sessions()
    FailedLoginAttempt.cleanup_old_attempts()
    
    # Get recent failed login attempts for security monitoring
    recent_failed_attempts = FailedLoginAttempt.query.order_by(
        FailedLoginAttempt.attempted_at.desc()
    ).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         items=items, 
                         current_sort=sort_by,
                         active_sessions=active_sessions,
                         recent_failed_attempts=recent_failed_attempts)

@admin.route('/item/new', methods=['GET', 'POST'])
@login_required
def new_item():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price', type=float)
        is_sold = bool(request.form.get('is_sold'))

        item = Item(name=name, description=description, price=price, is_sold=is_sold)
        db.session.add(item)
        db.session.commit()

        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image = Image.open(file)
                
                # Automatically rotate to correct orientation using EXIF
                image = ImageOps.exif_transpose(image)
                
                image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                image.save(filepath, optimize=True, quality=85)
                item_image = ItemImage(item_id=item.id, filename=filename)
                db.session.add(item_image)
        db.session.commit()
        
        # Log item creation
        current_app.logger.info(f'User {current_user.username} created item: {name} (ID: {item.id})')
        
        flash('Item added successfully', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/item_form.html')

@admin.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.price = request.form.get('price', type=float)
        item.is_sold = bool(request.form.get('is_sold'))

        # Handle image deletions
        images_to_delete = request.form.getlist('delete_images')
        for img_id in images_to_delete:
            img = ItemImage.query.get(int(img_id))
            if img and img in item.images:
                # Delete the file from the uploads folder
                image_path = os.path.join(current_app.root_path, 'static', 'uploads', img.filename)
                # Only delete if not a protected static image
                if img.filename not in ['noimage.jpeg', 'demo.jpg']:
                    try:
                        if os.path.exists(image_path):
                            os.remove(image_path)
                    except Exception as e:
                        print(f"Error deleting file {img.filename}: {e}")
                else:
                    print(f"Skipped deleting protected image: {img.filename}")
                db.session.delete(img)
        db.session.commit()

        # Handle new uploads
        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                image = Image.open(file)
                
                # Automatically rotate to correct orientation using EXIF
                image = ImageOps.exif_transpose(image)
                
                image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                image.save(filepath, optimize=True, quality=85)
                new_img = ItemImage(filename=filename, item_id=item.id)
                db.session.add(new_img)
        db.session.commit()

        # Handle primary image selection
        primary_image_id = request.form.get('primary_image')
        if primary_image_id:
            for img in item.images:
                img.is_primary = (str(img.id) == primary_image_id)
            db.session.commit()

        # Log item update
        current_app.logger.info(f'User {current_user.username} updated item: {item.name} (ID: {item.id})')
        
        flash('Item updated successfully.', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/item_form.html', item=item)

@admin.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    # Delete associated image files from disk
    for img in item.images:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], img.filename)
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                current_app.logger.info(f"Deleted image file: {filepath}")
        except Exception as e:
            current_app.logger.error(f"Failed to delete {filepath}: {e}")

    # Log item deletion
    current_app.logger.info(f'User {current_user.username} deleted item: {item.name} (ID: {item.id})')
    
    # Then delete the item record and cascade delete images from DB
    db.session.delete(item)
    db.session.commit()

    flash('Item deleted along with its images', 'success')
    return redirect(url_for('admin.dashboard'))


@admin.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        image = Image.open(file)

        # Automatically rotate to correct orientation using EXIF
        image = ImageOps.exif_transpose(image)

        image.thumbnail((800, 600), Image.Resampling.LANCZOS)
        image.save(filepath, optimize=True, quality=85)
        return jsonify({'filename': filename}), 200

    return jsonify({'error': 'File type not allowed'}), 400

@admin.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    # Clear any existing flash messages when accessing the change password page
    # This prevents item-related messages from showing up here
    if request.method == 'GET':
        # Get and discard any existing messages to clear them
        from flask import get_flashed_messages
        get_flashed_messages()
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'danger')
        elif len(new_password) < 6:
            flash('New password must be at least 6 characters.', 'danger')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            
            # Log password change
            current_app.logger.info(f'User {current_user.username} changed password from {request.remote_addr}')
            
            flash('Password changed successfully.', 'success')
            return redirect(url_for('admin.dashboard'))

    return render_template('admin/change_password.html')

@admin.route('/site-settings', methods=['GET', 'POST'])
@login_required
def site_settings():
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        settings.site_name = request.form.get('site_name', '').strip()
        settings.welcome_message = request.form.get('welcome_message', '').strip()
        settings.general_info = request.form.get('general_info', '').strip()
        settings.contact_info = request.form.get('contact_info', '').strip()
        
        # Validate required fields
        if not settings.site_name:
            flash('Site name is required.', 'danger')
        elif not settings.welcome_message:
            flash('Welcome message is required.', 'danger')
        elif not settings.general_info:
            flash('General information is required.', 'danger')
        elif not settings.contact_info:
            flash('Contact information is required.', 'danger')
        else:
            settings.updated_at = db.func.now()
            db.session.commit()
            
            # Log settings update
            current_app.logger.info(f'User {current_user.username} updated site settings')
            
            flash('Site settings updated successfully.', 'success')
            return redirect(url_for('admin.site_settings'))
    
    return render_template('admin/site_settings.html', settings=settings)

@admin.route('/logs')
@login_required
def view_logs():
    """View recent application logs (admin only)"""
    try:
        log_file = 'logs/flea_market.log'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                # Get last 100 lines
                lines = f.readlines()
                recent_logs = lines[-100:] if len(lines) > 100 else lines
                recent_logs.reverse()  # Show newest first
        else:
            recent_logs = ['No log file found']
        
        current_app.logger.info(f'User {current_user.username} viewed application logs')
        return render_template('admin/logs.html', logs=recent_logs)
        
    except Exception as e:
        current_app.logger.error(f'Error reading log file: {str(e)}')
        flash('Error reading log file', 'danger')
        return redirect(url_for('admin.dashboard'))
