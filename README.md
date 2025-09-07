# Flea Market App

A simple web application for managing and displaying items for sale in a local flea market (loppis in Sweden).  
Admins can add, edit, and delete items, upload images, and manage users.  
Visitors can browse available items and contact the seller using the information you decide to share. 

---

## Some Features

- Add, edit, and delete items with images, search
- Mark items as sold, manage image priority, click counter
- Admin panel
- Multi-language support 
- Mobile friendly
---

## Built on

- Python 3.8+
- Flask Components
- Pillow

---

## Local Installation

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
   
   **ENVs Explained:**
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
   For local dev work you have to do this. For the containerized version it is part of the startup scrip in Dockerfile.

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

## Docker Installation

You can also run the app using Docker. Build the image yourself with the attached Dockerfile or use my pre-built image.

I built a cross platform image on dockerhub so you can just run it with:

```sh
docker run -d -p 8111:5000 \
--name loppis \
-v flea-market-uploads:/app/app/static/uploads \
-v flea-market-db:/app/instance \
-v logs:/app/logs \
-e FLASK_ENV=production \
-e SECRET_KEY=your-production-secret-key-here \
-e ADMIN_USERNAME=admin \
-e ADMIN_PASSWORD=your-secure-password \
smintik/flea-market-app:latest
```

Docker Compose File
```bash
version: '3.8'

services:
  flea-market:
    image: smintik/flea-market-app:latest
    container_name: loppis
    ports:
      - "8111:5000"
    volumes:
      - uploads:/app/app/static/uploads
      - db:/app/instance
      - logs:/app/logs 
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=somethingsomethingelse
      - ADMIN_USERNAME=admin
      - ADMIN_PASSWORD=something-secure
    restart: unless-stopped

volumes:
  uploads:
  db:
  logs:
```

It will create a container listening on port 8111. There are persistent volumes:
- `flea-market-uploads` - Stores uploaded item images
- `flea-market-db` - Stores the SQLite database file
- `logs` - Stores the logs that can be viewed also from the ui

---

## Multi-Language

The app supports multiple languages with  switching via the admin panel. Compiled are Swedish and English. Currency as well as default language is a global setting you set in the site configuration panel.

### For Devs

Lot of this code has been generated using AI Coding Assistant, so things might not be optimal in some cases. 

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

How to use this:

1. **In Templates**:
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
   # Edit translations
   nano app/translations/sv/LC_MESSAGES/messages.po
   nano app/translations/en/LC_MESSAGES/messages.po
   ...
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

**Key Support Scripts / Files**:
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
- Some characters (å, ä, ö) are converted to ASCII-safe versions if needed
- Check `app/translations_fallback.py` for emergency translations

I have to work more on these special characters

---

## License

MIT License or whatever...

---

## Credits

I developed this using some AI tools so kudos to all the devs before me whos code was use to train the models.
