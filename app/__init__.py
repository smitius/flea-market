from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()
site_name = os.getenv('SITE_NAME', 'Personal Flea Market')
whatsapp_number = os.getenv('WHATSAPP_NUMBER', 'N/A')
apartment_address = os.getenv('APARTMENT_ADDRESS', 'N/A')

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    print("Flask app.root_path:", app.root_path)  # <-- Add this line
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/instance/flea_market.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['SITE_NAME'] = os.getenv('SITE_NAME', 'Personal Flea Market')
    app.config['WHATSAPP_NUMBER'] = os.getenv('WHATSAPP_NUMBER', '')
    app.config['APARTMENT_ADDRESS'] = os.getenv('APARTMENT_ADDRESS', '')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.routes.main import main
    from app.routes.auth import auth
    from app.routes.admin import admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(admin, url_prefix='/admin')

    with app.app_context():
        db.create_all()

    return app
