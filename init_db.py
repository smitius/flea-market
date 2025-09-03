import os
from app import create_app, db

from dotenv import load_dotenv
load_dotenv()

app = create_app()
app.app_context().push()

# Import models AFTER app context is pushed, but BEFORE db.create_all()
from app.models import User, Item, ItemImage  # Make sure you import ItemImage if you use it
from sqlalchemy import inspect

db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
print("DB Path: " + db_path)

db_exists = os.path.exists(db_path)
inspector = inspect(db.engine)
tables = inspector.get_table_names()
print(f"Tables found before create_all: {tables}")

if not db_exists or not tables:
    db.create_all()
    print("Database created.")
    # Refresh inspector and tables after creation
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables found after create_all: {tables}")
else:
    print("Database file and tables found, skipping create_all.")

if 'user' in tables:
    first_user = User.query.first()
    print(f"First user in DB: {first_user}")
    if first_user is None:
        admin_username = os.getenv('ADMIN_USERNAME', 'admin')
        admin_password = os.getenv('ADMIN_PASSWORD', 'demo')

        user = User(username=admin_username)
        user.set_password(admin_password)
        db.session.add(user)
        db.session.commit()
        print(f"Admin user '{admin_username}' created.")
    else:
        print("Admin user exists, skipping creation.")
else:
    print("User table does not exist!")

if 'item' in tables and Item.query.first() is None:
    demo_item = Item(
        name="Vacker vas",
        description="En vacker vas i keramik, perfekt för blommor eller som dekoration.",
        price=120.00,
        is_sold=False
    )
    db.session.add(demo_item)
    db.session.commit()
    print("Demo item created.")

    # Add image if ItemImage model is used
    demo_image_path = "demo.jpg"  # relative to static folder if you use url_for('static', ...)
    if os.path.exists(os.path.join(app.root_path, 'static', demo_image_path)):
        demo_image = ItemImage(
            filename="demo.jpg",
            item_id=demo_item.id
        )
        db.session.add(demo_image)
        db.session.commit()
        print("Demo image linked to demo item.")
    else:
        print("Demo image not found, skipping image link.")

else:
    print("Demo item already exists or item table missing.")

print("Initialization complete.")
