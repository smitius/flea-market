from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

user = User(username='admin')
user.set_password('demo')  # Change the password to a secure one

db.session.add(user)
db.session.commit()

print("Admin user created.")
exit()
