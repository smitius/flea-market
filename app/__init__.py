from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_babel import Babel
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import timedelta
from config import Config
from version import APP_NAME, APP_VERSION

db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
babel = Babel()

def create_app():
    load_dotenv()  

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    
    # Session configuration
    app.permanent_session_lifetime = timedelta(hours=2)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)

    # Set these in app.config so they're available everywhere
    app.config['SITE_NAME'] = os.getenv('SITE_NAME', 'Personal Flea Market')
    app.config['WHATSAPP_NUMBER'] = os.getenv('WHATSAPP_NUMBER', 'N/A')
    app.config['APARTMENT_ADDRESS'] = os.getenv('APARTMENT_ADDRESS', 'N/A')
    app.config['APP_NAME'] = APP_NAME
    app.config['APP_VERSION'] = APP_VERSION

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    limiter.init_app(app)
    
    # Update session activity on each request
    @app.before_request
    def update_session_activity():
        from flask_login import current_user
        from flask import session
        if current_user.is_authenticated and 'session_id' in session:
            from app.models import UserSession
            user_session = UserSession.query.filter_by(
                session_id=session['session_id'],
                user_id=current_user.id,
                is_active=True
            ).first()
            if user_session:
                user_session.last_activity = db.func.now()
                db.session.commit()

    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.admin import admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    def get_locale():
        try:
            from app.models import SiteSettings
            settings = SiteSettings.get_settings()
            return settings.language if settings else 'sv'
        except:
            return 'sv'
    
    # Configure Babel with proper encoding
    app.config['LANGUAGES'] = {
        'sv': 'Svenska',
        'en': 'English'
    }
    app.config['BABEL_DEFAULT_LOCALE'] = 'sv'
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
    
    babel.init_app(app, locale_selector=get_locale)
    
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convert newlines to HTML line breaks"""
        if not text:
            return text
        return text.replace('\n', '<br>')
    
    @app.template_filter('currency')
    def currency_filter(amount, currency=None):
        """Format currency based on site settings"""
        from app.models import SiteSettings
        if currency is None:
            settings = SiteSettings.get_settings()
            currency = settings.currency if settings else 'SEK'
        
        if currency == 'SEK':
            return f"{amount:.2f} Kr"
        elif currency == 'USD':
            return f"${amount:.2f}"
        else:
            return f"{amount:.2f} {currency}"
    
    @app.context_processor
    def inject_app_info():
        from app.models import SiteSettings
        settings = SiteSettings.get_settings()
        
        # Safe translation function with fallback
        def safe_gettext(text):
            try:
                from flask_babel import gettext
                return gettext(text)
            except:
                # Fallback to our simple translation system
                from app.translations_fallback import get_translation
                language = settings.language if settings else 'sv'
                return get_translation(text, language)
        
        return dict(
            app_name=app.config['APP_NAME'],
            app_version=app.config['APP_VERSION'],
            settings=settings,
            _=safe_gettext  # Make safe translation function available in templates
        )

    # Configure logging
    configure_logging(app)
    
    # Add error handlers
    register_error_handlers(app)
    
    # Add security headers
    add_security_headers(app)

    return app

def configure_logging(app):
    """Configure application logging"""
    
    # Don't configure logging if we're in testing mode
    if app.testing:
        return
    
    # Set log level based on environment
    flask_env = os.getenv('FLASK_ENV', 'development')
    if flask_env == 'production':
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Configure file handler with rotation
    file_handler = RotatingFileHandler(
        'logs/flea_market.log', 
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(log_level)
    
    # Configure console handler for Docker logs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    console_handler.setLevel(log_level)
    
    # Clear existing handlers to avoid duplicates
    app.logger.handlers.clear()
    
    # Add handlers to app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # Don't prevent propagation in development
    if flask_env == 'production':
        app.logger.propagate = False
    
    # Log startup
    app.logger.info(f'{APP_NAME} v{APP_VERSION} startup')
    app.logger.info(f'Environment: {flask_env}')
    app.logger.info(f'Log level: {logging.getLevelName(log_level)}')

def register_error_handlers(app):
    """Register error handlers with logging"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import request, render_template
        app.logger.warning(f'404 error: {request.url} from {request.remote_addr}')
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import request, render_template
        app.logger.error(f'500 error: {request.url} from {request.remote_addr}', exc_info=True)
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(429)
    def ratelimit_handler(error):
        from flask import request, render_template
        app.logger.warning(f'Rate limit exceeded: {request.url} from {request.remote_addr}')
        return render_template('errors/429.html'), 429
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        from flask import request, render_template
        app.logger.error(f'Unhandled exception: {request.url} from {request.remote_addr}', exc_info=True)
        db.session.rollback()
        return render_template('errors/500.html'), 500

def add_security_headers(app):
    """Add security headers to all responses"""
    
    @app.after_request
    def set_security_headers(response):
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'DENY'
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # XSS protection
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Content Security Policy (basic)
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "font-src 'self' https://cdnjs.cloudflare.com; "
            "img-src 'self' data:; "
            "connect-src 'self';"
        )
        
        return response
