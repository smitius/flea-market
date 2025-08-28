import os
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_required
from werkzeug.utils import secure_filename
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
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('admin/dashboard.html', items=items)

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

        db.session.commit()
        flash('Item updated successfully')
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
