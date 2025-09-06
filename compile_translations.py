#!/usr/bin/env python3
"""
Compile translation files from .po to .mo format.
This script converts human-readable .po files to binary .mo files that Flask uses.

Usage:
    python compile_translations.py

This will compile all translation files in app/translations/*/LC_MESSAGES/
"""

import os
import sys

def compile_translations():
    """Compile all translation files"""
    
    print("🔨 Compiling translation files...")
    
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
    
    print("🚀 Restart your Flask app to see the changes")
    return True

if __name__ == '__main__':
    success = compile_translations()
    sys.exit(0 if success else 1)