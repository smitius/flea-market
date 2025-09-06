from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    is_sold = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    view_count = db.Column(db.Integer, default=0)
    images = db.relationship('ItemImage', backref='item', lazy=True, cascade='all, delete-orphan')

class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), nullable=False, default='Vår egen Loppis')
    welcome_message = db.Column(db.String(200), nullable=False, default='Hej och Välkommen')
    general_info = db.Column(db.Text, nullable=False, default='Vi rensar ut några saker vi inte längre behöver – och det kan vara precis vad du letar efter.')
    contact_info = db.Column(db.Text, nullable=False, default='Kontakta oss för mer information.')
    language = db.Column(db.String(5), nullable=False, default='sv')  # 'sv' or 'en'
    currency = db.Column(db.String(3), nullable=False, default='SEK')  # 'SEK' or 'USD'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @staticmethod
    def get_settings():
        """Get the current site settings, create default if none exist"""
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
        return settings

class UserSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_id = db.Column(db.String(255), nullable=False, unique=True)
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
    
    @staticmethod
    def cleanup_expired_sessions():
        """Remove sessions older than 2 hours (or 7 days for remembered sessions)"""
        from datetime import timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=2)
        expired_sessions = UserSession.query.filter(
            UserSession.last_activity < cutoff_time,
            UserSession.is_active == True
        ).all()
        
        for session in expired_sessions:
            session.is_active = False
        
        db.session.commit()
        return len(expired_sessions)

class FailedLoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(80))
    user_agent = db.Column(db.Text)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def is_ip_blocked(ip_address, minutes=15, max_attempts=5):
        """Check if IP should be blocked due to too many failed attempts"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        recent_attempts = FailedLoginAttempt.query.filter(
            FailedLoginAttempt.ip_address == ip_address,
            FailedLoginAttempt.attempted_at > cutoff_time
        ).count()
        return recent_attempts >= max_attempts
    
    @staticmethod
    def cleanup_old_attempts(days=7):
        """Clean up old failed login attempts"""
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        old_attempts = FailedLoginAttempt.query.filter(
            FailedLoginAttempt.attempted_at < cutoff_time
        ).delete()
        db.session.commit()
        return old_attempts
