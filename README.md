# Flea Market App

A simple web application for managing and displaying items for sale in a local flea market (loppis in Sweden).  
Admins can add, edit, and delete items, upload images, and manage users.  
Visitors can browse available items and contact the seller using the information you decide to share. 

---

## Features

- Add, edit, and delete items with images
- Mark items as sold
- Multiple images per item, with primary image selection
- Admin authentication and password management
- **View counter** - Track how many times each item is viewed
- **Site settings management** - Edit site name, welcome message, and contact info from admin panel
- Demo item and image on first run
- Responsive design

---

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Dotenv
- Pillow

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/flea-market-app.git
   cd flea-market-app
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file with the following required variables:
     ```
     FLASK_ENV=development
     SECRET_KEY=your-super-secret-random-string-here-32chars-minimum
     ADMIN_USERNAME=admin
     ADMIN_PASSWORD=your-secure-password
     ```
   
   **Environment Variables Explained:**
   - `FLASK_ENV`: Controls Flask's runtime behavior
     - `development` - Enables debug mode, auto-reload, detailed error pages (for local development)
     - `production` - Optimized performance, generic error pages (for live deployment)
   - `SECRET_KEY`: Cryptographic key for session security, flash messages, and CSRF protection
     - Must be random and unpredictable (at least 32 characters)
     - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
     - Use different keys for development and production
   - `ADMIN_USERNAME`: Username for admin login
   - `ADMIN_PASSWORD`: Password for admin login (change from default!)

5. **Initialize the database:**
   ```sh
   python init_db.py
   ```
   This script will:
   - Create the database file and tables
   - Create the admin user with credentials from your `.env` file
   - Add a demo item with sample image
   - Initialize default site settings (editable later from admin panel)

6. **Run the app:**
   ```sh
   flask run
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000).

---

## Docker

You can also run the app using Docker:

I built an image so you can just run it with:

```sh
docker run -d -p 8111:5000 \
-v flea-market-uploads:/app/app/static/uploads \
-v flea-market-db:/app/instance \
-e FLASK_ENV=production \
-e SECRET_KEY=your-production-secret-key-here \
-e ADMIN_USERNAME=admin \
-e ADMIN_PASSWORD=your-secure-password \
smintik/flea-market-app:latest
```
It will create a container listening on port 8111. There are two persistent volumes:
- `flea-market-uploads` - Stores uploaded item images
- `flea-market-db` - Stores the SQLite database file

**Note:** Site content (name, welcome message, contact info) is now managed through the admin panel at `/admin/site-settings` instead of environment variables. 

---

## Configuration

- App name and version are set in `app/version.py`.
- Images are stored in `app/static/uploads/`.
- Default and demo images are in `app/static/`.

---

## Usage

### Admin Features
- Visit `/admin` to log in as admin
- **Dashboard**: Add, edit, delete items and view item statistics (view counts)
- **Site Settings**: Customize site name, welcome message, general info, and contact information
- **Change Password**: Update your admin password securely

### Visitor Experience
- Browse available items with image galleries
- View item details by clicking on items (automatically tracked)
- Contact seller using the information provided in site settings

### Database Migration
If upgrading from an older version, run the migration scripts:
```sh
python migrate_add_view_count.py      # Adds view counter feature
python migrate_add_site_settings.py   # Adds site settings management
```

---

## License

MIT License or whatever...

---

## Credits

I developed this using some AI tools help and a bit of time. It was fun and it is useful to me, it might be to you too. 
