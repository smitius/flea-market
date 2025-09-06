from flask import Blueprint, render_template, jsonify, current_app, request, session, redirect, url_for
from app.models import Item, SiteSettings
from app import db, limiter

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

@main.route('/set-language/<language>')
@limiter.limit("10 per minute")  # Rate limit to prevent abuse
def set_language(language):
    """
    Set the user's language preference for UI translations only
    
    This route handles language switching for users and implements the following features:
    - Validates language codes against supported languages
    - Stores preference in session for persistence (Requirement 1.4)
    - Falls back to admin-configured default for invalid codes (Requirement 1.6)
    - Supports both regular HTTP and JSON API requests
    - Includes rate limiting and comprehensive error handling
    
    Note: Currency is NOT automatically switched - it remains as configured in site settings
    
    Args:
        language (str): Language code (e.g., 'sv', 'en')
        
    Returns:
        Redirect response for regular requests or JSON response for API requests
    """
    from app.models import SiteSettings
    
    # Get supported languages from app config
    supported_languages = current_app.config.get('LANGUAGES', {}).keys()
    
    # Validate language code
    if language not in supported_languages:
        current_app.logger.warning(f'Invalid language code attempted: {language} from {request.remote_addr}')
        # Fallback to admin-configured default language
        settings = SiteSettings.get_settings()
        language = settings.language if settings else 'sv'
        
        # Clear any existing invalid language session data
        if 'user_language' in session:
            del session['user_language']
    
    try:
        # Store language preference in session
        session['user_language'] = language
        session.permanent = True  # Make session persistent
        
        # Log successful language change
        current_app.logger.info(f'Language changed to {language} from {request.remote_addr}')
        
        # Return JSON response for AJAX requests
        if request.headers.get('Content-Type') == 'application/json' or request.is_json:
            return jsonify({
                'success': True,
                'language': language,
                'message': 'Language preference updated successfully'
            })
        
    except Exception as e:
        current_app.logger.error(f'Error setting language preference: {str(e)} from {request.remote_addr}')
        
        # Return error response for AJAX requests
        if request.headers.get('Content-Type') == 'application/json' or request.is_json:
            return jsonify({
                'success': False,
                'error': 'Failed to update language preference'
            }), 500
        
        # For regular requests, continue with fallback
        pass
    
    # Redirect back to the referring page or home
    return redirect(request.referrer or url_for('main.index'))

@main.route('/language-status')
def language_status():
    """
    Get current language and currency status for the user
    
    This endpoint provides information about the user's current language and currency
    preferences, as well as available options and site defaults. Useful for frontend
    components that need to display current state or available options.
    
    Returns:
        JSON response with current language, currency, supported languages, and defaults
    """
    from app.models import SiteSettings
    
    try:
        settings = SiteSettings.get_settings()
        current_language = session.get('user_language')
        
        # If no user language preference, use site default
        if not current_language:
            current_language = settings.language if settings else 'sv'
        
        # Currency is always from site settings (no user preference)
        site_currency = settings.currency if settings else 'SEK'
        
        return jsonify({
            'success': True,
            'current_language': current_language,
            'site_currency': site_currency,
            'supported_languages': current_app.config.get('LANGUAGES', {}),
            'site_default_language': settings.language if settings else 'sv'
        })
        
    except Exception as e:
        current_app.logger.error(f'Error getting language status: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Failed to get language status'
        }), 500