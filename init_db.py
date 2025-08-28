import os
from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flea_market.db')

if not os.path.exists(db_path):
    db.create_all()
    print("Database created.")
else:
    print("Database file found, skipping create_all.")

if User.query.first() is None:
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'demo')

    user = User(username=admin_username)
    user.set_password(admin_password)
    db.session.add(user)
    db.session.commit()
    print(f"Admin user '{admin_username}' created.")
else:
    print("Admin user exists, skipping creation.")

print("Initialization complete.")
