from flask import Blueprint, render_template, jsonify, current_app, request
from app.models import Item, SiteSettings
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Get search and sort parameters
    search_query = request.args.get('search', '').strip()
    sort_by = request.args.get('sort', 'newest')
    
    # Start with base query
    query = Item.query
    
    # Apply search filter if provided
    if search_query:
        query = query.filter(
            db.or_(
                Item.name.ilike(f'%{search_query}%'),
                Item.description.ilike(f'%{search_query}%')
            )
        )
    
    # Apply sorting
    if sort_by == 'oldest':
        query = query.order_by(Item.created_at.asc())
    elif sort_by == 'price_low':
        query = query.order_by(Item.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Item.price.desc())
    elif sort_by == 'name':
        query = query.order_by(Item.name.asc())
    elif sort_by == 'views':
        query = query.order_by(Item.view_count.desc())
    else:  # newest (default)
        query = query.order_by(Item.created_at.desc())
    
    items = query.all()
    settings = SiteSettings.get_settings()
    
    return render_template(
        'index.html', 
        items=items,
        settings=settings,
        search_query=search_query,
        current_sort=sort_by
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