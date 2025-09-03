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
   - Copy `.env.example` to `.env` and edit as needed, or create a `.env` file:
     ```
     FLASK_ENV=development
     SECRET_KEY=your-secret-key
     SITE_NAME=Your Flea Market
     WHATSAPP_NUMBER=+46701234567
     APARTMENT_ADDRESS=Your Address
     ADMIN_USERNAME=admin
     ADMIN_PASSWORD=admin
     ```

5. **Initialize the database:**
   ```sh
   python init_db.py
   ```
This is mostly for running it localy or testing. The script will initiate the DB file, create admin user and a demo item.

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
docker run -d -p 8111:5000 `
-v flea-market-uploads:/app/app/static/uploads `
-v flea-market-db:/app/instance `
-e FLASK_ENV=production `
-e SECRET_KEY=somethingsomethingelse `
-e ADMIN_USERNAME=admin `
-e ADMIN_PASSWORD=admin `
-e SITE_NAME="something" `
-e WHATSAPP_NUMBER="+4670777777" `
-e APARTMENT_ADDRESS="something else" `
smintik/flea-market-app:latest
```
It will create a container listening on port 8111. There are two persistent volumes one for the images attached to the items and one for the DB file. 

Note: the envs are a bit of a mess with naming but you get basically 3 inputs to modify the text on the main page. Mostly for people to know how to contact you. I might need to rework that in the future and put it into the admin form. 

---

## Configuration

- App name and version are set in `app/version.py`.
- Images are stored in `app/static/uploads/`.
- Default and demo images are in `app/static/`.

---

## Usage

- Visit `/admin` to log in as admin.
- Use the dashboard to add, edit, or delete items.
- Change your admin password from the dashboard.
- Visitors can browse items and contact you using the instructions you provide or in person if you wish.

---

## License

MIT License or whatever...

---

## Credits

I developed this using some AI tools help and a bit of time. It was fun and it is useful to me, it might be to you too. 
