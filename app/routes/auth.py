from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, UserSession
from app import db
import uuid

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            # Create session tracking
            session_id = str(uuid.uuid4())
            session['session_id'] = session_id
            
            user_session = UserSession(
                user_id=user.id,
                session_id=session_id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')[:500]  # Limit length
            )
            db.session.add(user_session)
            db.session.commit()
            
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    # Mark session as inactive
    if 'session_id' in session:
        user_session = UserSession.query.filter_by(
            session_id=session['session_id'],
            user_id=current_user.id
        ).first()
        if user_session:
            user_session.is_active = False
            db.session.commit()
    
    logout_user()
    return redirect(url_for('main.index'))
