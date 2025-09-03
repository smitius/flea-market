from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from config import Config
from version import APP_NAME, APP_VERSION

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()  # <-- Ensure .env is loaded here

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')

    # Set these in app.config so they're available everywhere
    app.config['SITE_NAME'] = os.getenv('SITE_NAME', 'Personal Flea Market')
    app.config['WHATSAPP_NUMBER'] = os.getenv('WHATSAPP_NUMBER', 'N/A')
    app.config['APARTMENT_ADDRESS'] = os.getenv('APARTMENT_ADDRESS', 'N/A')
    app.config['APP_NAME'] = APP_NAME
    app.config['APP_VERSION'] = APP_VERSION

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.admin import admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    @app.context_processor
    def inject_app_info():
        return dict(
            app_name=app.config['APP_NAME'],
            app_version=app.config['APP_VERSION']
        )

    return app
