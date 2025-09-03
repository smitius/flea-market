import os
from app import create_app

app = create_app()

with app.app_context():
    print(f"Flask app root path: {app.root_path}")
    print(f"Flask instance path: {app.instance_path}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Instance path exists: {os.path.exists(app.instance_path)}")
    
    # Check if we can create files in instance path
    try:
        test_file = os.path.join(app.instance_path, 'test.txt')
        os.makedirs(app.instance_path, exist_ok=True)
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        print("Instance path is writable: YES")
    except Exception as e:
        print(f"Instance path is writable: NO - {e}")
