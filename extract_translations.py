#!/usr/bin/env python3
"""
Extract translatable strings from templates and Python files.
This script scans the codebase for _('text') patterns and updates translation files.

Usage:
    python extract_translations.py

This will:
1. Extract all translatable strings to messages.pot
2. Update existing translation files (.po)
3. Create new language files if they don't exist
"""

import os
import sys

def extract_and_update_translations():
    """Extract strings and update translation files"""
    
    print("🔍 Extracting translatable strings from templates and Python files...")
    
    # Extract strings to messages.pot template file
    result = os.system('pybabel extract -F babel.cfg -k _ -o messages.pot .')
    if result != 0:
        print("❌ Failed to extract strings. Make sure Flask-Babel is installed.")
        return False
    
    # Update Swedish translation
    if not os.path.exists('app/translations/sv'):
        print("🇸🇪 Creating Swedish translation...")
        os.system('pybabel init -i messages.pot -d app/translations -l sv')
    else:
        print("🇸🇪 Updating Swedish translation...")
        os.system('pybabel update -i messages.pot -d app/translations')
    
    # Update English translation
    if not os.path.exists('app/translations/en'):
        print("🇺🇸 Creating English translation...")
        os.system('pybabel init -i messages.pot -d app/translations -l en')
    else:
        print("🇺🇸 Updating English translation...")
        os.system('pybabel update -i messages.pot -d app/translations')
    
    # Update Slovak translation
    if not os.path.exists('app/translations/sk'):
        print("🇸🇰 Creating Slovak translation...")
        os.system('pybabel init -i messages.pot -d app/translations -l sk')
    else:
        print("🇸🇰 Updating Slovak translation...")
        os.system('pybabel update -i messages.pot -d app/translations')
    
    # Update Czech translation
    if not os.path.exists('app/translations/cs'):
        print("🇨🇿 Creating Czech translation...")
        os.system('pybabel init -i messages.pot -d app/translations -l cs')
    else:
        print("🇨🇿 Updating Czech translation...")
        os.system('pybabel update -i messages.pot -d app/translations')
    
    print("✅ Translation files updated!")
    print("\n📝 Next steps:")
    print("1. Edit app/translations/sv/LC_MESSAGES/messages.po for Swedish translations")
    print("2. Edit app/translations/en/LC_MESSAGES/messages.po for English translations")
    print("3. Edit app/translations/sk/LC_MESSAGES/messages.po for Slovak translations")
    print("4. Edit app/translations/cs/LC_MESSAGES/messages.po for Czech translations")
    print("5. Run 'python compile_translations.py' to compile the changes")
    print("6. Restart your Flask app to see the updates")
    
    return True

if __name__ == '__main__':
    success = extract_and_update_translations()
    sys.exit(0 if success else 1)