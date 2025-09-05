from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from datetime import timedelta
from config import Config
from version import APP_NAME, APP_VERSION

db = SQLAlchemy()
login_manager = LoginManager()

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

    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convert newlines to HTML line breaks"""
        if not text:
            return text
        return text.replace('\n', '<br>')
    
    @app.context_processor
    def inject_app_info():
        from app.models import SiteSettings
        settings = SiteSettings.get_settings()
        return dict(
            app_name=app.config['APP_NAME'],
            app_version=app.config['APP_VERSION'],
            settings=settings
        )

    return app
