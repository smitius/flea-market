from flask import Blueprint, render_template, jsonify, current_app, request
from app.models import Item, SiteSettings
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    settings = SiteSettings.get_settings()
    return render_template(
        'index.html', 
        items=items,
        settings=settings
    )

@main.route('/item/<int:item_id>/view', methods=['POST'])
def track_item_view(item_id):
    """Track when an item is viewed by incrementing its view count"""
    item = Item.query.get_or_404(item_id)
    item.view_count += 1
    db.session.commit()
    
    # Log item view (debug level to avoid spam)
    current_app.logger.debug(f'Item viewed: {item.name} (ID: {item_id}) from {request.remote_addr}')
    
    return jsonify({'success': True, 'view_count': item.view_count})