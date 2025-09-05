from flask import Blueprint, render_template, jsonify
from app.models import Item
from app import db
from flask import current_app as app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template(
        'index.html', 
        items=items,
        site_name=app.config.get('SITE_NAME', 'Personal Flea Market'),
        whatsapp_number=app.config.get('WHATSAPP_NUMBER', ''),
        apartment_address=app.config.get('APARTMENT_ADDRESS', '')
    )

@main.route('/item/<int:item_id>/view', methods=['POST'])
def track_item_view(item_id):
    """Track when an item is viewed by incrementing its view count"""
    item = Item.query.get_or_404(item_id)
    item.view_count += 1
    db.session.commit()
    return jsonify({'success': True, 'view_count': item.view_count})