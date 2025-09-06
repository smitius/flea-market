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
- **Multi-language support** - Swedish and English with automatic currency switching
- **Modern mobile navigation** - Responsive slide-out menu and touch-friendly interface
- **Advanced image gallery** - Swipe navigation, pinch-to-zoom, and fullscreen viewing
- Demo item and image on first run
- Responsive design with mobile-first approach

---

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Babel (for multi-language support)
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
--name loppis \
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

### Docker Management Commands
```sh
# Stop the container
docker stop loppis

# Start the container
docker start loppis

# View logs
docker logs loppis

# Remove container (keeps volumes)
docker rm loppis

# Remove container and volumes (⚠️ deletes all data)
docker rm loppis && docker volume rm flea-market-uploads flea-market-db
``` 

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

## Multi-Language Support

The app supports multiple languages with easy switching via the admin panel.

### Supported Languages
- **Swedish (Svenska)** - Default language
- **English** - Full translation available

### Supported Currencies
- **SEK (Swedish Krona)** - "123.45 Kr" format
- **USD (US Dollar)** - "$123.45" format

### For Users
1. **Admin Access**: Go to Admin → Site Settings
2. **Language Selection**: Choose between Svenska and English
3. **Currency Selection**: Choose between SEK and USD
4. **Auto-Currency**: Language selection automatically suggests appropriate currency

### For Developers

#### Translation Architecture
The app uses Flask-Babel for internationalization with a fallback system:
- **Primary**: Flask-Babel with compiled .mo files
- **Fallback**: Simple Python dictionary in `app/translations_fallback.py`
- **Error Handling**: Graceful degradation if translations fail

#### File Structure
```
app/translations/
├── sv/LC_MESSAGES/
│   ├── messages.po    # Swedish translations (human-readable)
│   └── messages.mo    # Swedish compiled translations
├── en/LC_MESSAGES/
│   ├── messages.po    # English translations (human-readable)
│   └── messages.mo    # English compiled translations
└── babel.cfg          # Babel configuration
```

#### Adding New Translatable Text

1. **In Templates**: Use the translation function
   ```html
   <!-- Before -->
   <h1>Contact</h1>
   
   <!-- After -->
   <h1>{{ _('Contact') }}</h1>
   ```

2. **In Python Code**: Import and use gettext
   ```python
   from flask_babel import gettext as _
   flash(_('Item deleted successfully'), 'success')
   ```

3. **Extract New Strings**: Run the extraction script
   ```bash
   python extract_translations.py
   ```

4. **Edit Translation Files**: Update the .po files
   ```bash
   # Edit Swedish translations
   nano app/translations/sv/LC_MESSAGES/messages.po
   
   # Edit English translations  
   nano app/translations/en/LC_MESSAGES/messages.po
   ```

5. **Compile Translations**: Generate .mo files
   ```bash
   python compile_translations.py
   ```

6. **Restart App**: Restart Flask to load new translations

#### Adding New Languages

1. **Create Language Directory**:
   ```bash
   mkdir -p app/translations/[LANG_CODE]/LC_MESSAGES
   ```

2. **Copy Base Translation File**:
   ```bash
   cp app/translations/sv/LC_MESSAGES/messages.po app/translations/[LANG_CODE]/LC_MESSAGES/
   ```

3. **Translate Strings**: Edit the new .po file with translations

4. **Update Admin Interface**: Add language option in `app/templates/admin/site_settings.html`

5. **Update Validation**: Add language code to validation in `app/routes/admin.py`

6. **Compile and Test**: Run `python compile_translations.py` and test

#### Translation Files Explained

**messages.po Format**:
```po
# Comment explaining context
msgid "Original English text"
msgstr "Translated text"

msgid "Delete this item?"
msgstr "Ta bort denna vara?"
```

**Key Files**:
- `extract_translations.py` - Scans code for translatable strings
- `compile_translations.py` - Converts .po files to .mo files  
- `create_safe_translations.py` - Fallback compilation method
- `app/translations_fallback.py` - Emergency fallback translations
- `babel.cfg` - Babel configuration for extraction

#### Troubleshooting Translations

**Translations not showing**:
1. Check if .mo files exist: `ls app/translations/*/LC_MESSAGES/messages.mo`
2. Recompile: `python compile_translations.py`
3. Restart Flask app
4. Check browser language settings

**Adding new strings**:
1. Add `{{ _('New Text') }}` in templates
2. Run `python extract_translations.py`
3. Edit .po files with translations
4. Run `python compile_translations.py`
5. Restart app

**Encoding issues**:
- The app includes fallback translations to handle encoding problems
- Swedish characters (å, ä, ö) are converted to ASCII-safe versions if needed
- Check `app/translations_fallback.py` for emergency translations

---

## License

MIT License or whatever...

---

## Credits

I developed this using some AI tools help and a bit of time. It was fun and it is useful to me, it might be to you too. 
