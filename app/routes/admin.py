import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from PIL import Image, ImageOps
from app import db
from app.models import Item, ItemImage

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
    
    return render_template('admin/dashboard.html', items=items, current_sort=sort_by)

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
                image.thumbnail((800, 600), Image.Resampling.LANCZOS)
                image.save(filepath, optimize=True, quality=85)
                item_image = ItemImage(item_id=item.id, filename=filename)
                db.session.add(item_image)
        db.session.commit()
        flash('Item added successfully')
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
                file.save(os.path.join(current_app.root_path, 'static/uploads', filename))
                new_img = ItemImage(filename=filename, item_id=item.id)
                db.session.add(new_img)
        db.session.commit()

        # Handle primary image selection
        primary_image_id = request.form.get('primary_image')
        if primary_image_id:
            for img in item.images:
                img.is_primary = (str(img.id) == primary_image_id)
            db.session.commit()

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

    # Then delete the item record and cascade delete images from DB
    db.session.delete(item)
    db.session.commit()

    flash('Item deleted along with its images')
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
            flash('Password changed successfully.', 'success')
            return redirect(url_for('admin.dashboard'))

    return render_template('admin/change_password.html')
