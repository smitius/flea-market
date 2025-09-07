#!/usr/bin/env python3
"""
Compile translation files from .po to .mo format.
This script converts human-readable .po files to binary .mo files that Flask uses.

Usage:
    python compile_translations.py

This will compile all translation files in app/translations/*/LC_MESSAGES/
Supports Swedish (sv), English (en), Slovak (sk), and Czech (cs) languages.
"""

import os
import sys

def compile_translations():
    """Compile all translation files including Slovak and Czech"""
    
    print("🔨 Compiling translation files...")
    
    # Define supported languages
    supported_languages = ['sv', 'en', 'sk', 'cs']
    
    # Try using pybabel first (preferred method)
    result = os.system('pybabel compile -d app/translations')
    
    if result != 0:
        print("⚠️  pybabel compile failed, trying fallback method...")
        # Fallback to our safe compilation method
        try:
            from create_safe_translations import create_safe_translations
            create_safe_translations()
            print("✅ Translation files compiled using fallback method!")
        except Exception as e:
            print(f"❌ Compilation failed: {e}")
            return False
    else:
        print("✅ Translation files compiled successfully!")
    
    # Verify that all supported languages have been processed
    print("🔍 Verifying compilation for all supported languages...")
    missing_languages = []
    
    for lang in supported_languages:
        mo_file_path = f"app/translations/{lang}/LC_MESSAGES/messages.mo"
        if os.path.exists(mo_file_path):
            print(f"  ✅ {lang}: messages.mo found")
        else:
            print(f"  ⚠️  {lang}: messages.mo missing")
            missing_languages.append(lang)
    
    if missing_languages:
        print(f"⚠️  Missing .mo files for languages: {', '.join(missing_languages)}")
        print("   These languages will fall back to the translation fallback system.")
    
    print("🚀 Restart your Flask app to see the changes")
    return True

if __name__ == '__main__':
    success = compile_translations()
    sys.exit(0 if success else 1)