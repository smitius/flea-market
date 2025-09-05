from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, UserSession, FailedLoginAttempt
from app import db, limiter
import uuid
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", methods=["POST"], 
               error_message="Too many login attempts. Please wait before trying again.")
def login():
    if request.method == 'POST':
        # Check if IP is blocked due to too many failed attempts
        if FailedLoginAttempt.is_ip_blocked(request.remote_addr):
            current_app.logger.warning(f'Blocked login attempt from {request.remote_addr} - too many failed attempts')
            flash('Too many failed login attempts. Please try again later.', 'danger')
            return render_template('login.html'), 429

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
            
            # Log successful login
            current_app.logger.info(f'User {username} logged in successfully from {request.remote_addr}')
            
            return redirect(url_for('admin.dashboard'))
        else:
            try:
                # Record failed login attempt
                failed_attempt = FailedLoginAttempt(
                    ip_address=request.remote_addr,
                    username=username,
                    user_agent=request.headers.get('User-Agent', '')[:500]
                )
                db.session.add(failed_attempt)
                db.session.commit()
                
                # Log failed login attempt
                current_app.logger.warning(f'Failed login attempt for username: {username} from {request.remote_addr}')
            except Exception as e:
                current_app.logger.error(f'Error recording failed login attempt: {str(e)}')
                db.session.rollback()
            
            flash('Invalid username or password')
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    # Log logout
    current_app.logger.info(f'User {current_user.username} logged out from {request.remote_addr}')
    
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
