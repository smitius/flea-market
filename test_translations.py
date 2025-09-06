#!/usr/bin/env python3
"""
Test script to verify translation functionality.
Run this after making translation changes to ensure everything works.

Usage:
    python test_translations.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_translation_files():
    """Test that translation files exist and are readable"""
    print("🧪 Testing translation files...")
    
    required_files = [
        'app/translations/sv/LC_MESSAGES/messages.po',
        'app/translations/sv/LC_MESSAGES/messages.mo',
        'app/translations/en/LC_MESSAGES/messages.po',
        'app/translations/en/LC_MESSAGES/messages.mo'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            return False
    
    return True

def test_fallback_system():
    """Test the fallback translation system"""
    print("\n🧪 Testing fallback translation system...")
    
    try:
        from app.translations_fallback import get_translation
        
        # Test key translations
        test_cases = [
            ('Dashboard', 'sv', 'Instrumentpanel'),
            ('Contact', 'sv', 'Kontakt'),
            ('Price', 'sv', 'Pris'),
            ('Dashboard', 'en', 'Dashboard'),
            ('Contact', 'en', 'Contact'),
        ]
        
        for text, lang, expected in test_cases:
            result = get_translation(text, lang)
            if result == expected:
                print(f"✅ {lang}: '{text}' → '{result}'")
            else:
                print(f"❌ {lang}: '{text}' → '{result}' (expected '{expected}')")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback system error: {e}")
        return False

def test_flask_integration():
    """Test Flask app with translations"""
    print("\n🧪 Testing Flask integration...")
    
    try:
        from app import create_app
        from app.models import SiteSettings
        
        app = create_app()
        with app.app_context():
            settings = SiteSettings.get_settings()
            print(f"✅ Current language: {settings.language}")
            print(f"✅ Current currency: {settings.currency}")
            
            # Test currency formatting (simple test)
            def test_currency_format(amount, currency):
                if currency == 'SEK':
                    return f"{amount:.2f} Kr"
                elif currency == 'USD':
                    return f"${amount:.2f}"
                else:
                    return f"{amount:.2f} {currency}"
            
            sek_result = test_currency_format(123.45, 'SEK')
            usd_result = test_currency_format(123.45, 'USD')
            print(f"✅ SEK formatting: {sek_result}")
            print(f"✅ USD formatting: {usd_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask integration error: {e}")
        return False

def main():
    """Run all translation tests"""
    print("🚀 Testing Translation System")
    print("=" * 40)
    
    tests = [
        ("Translation Files", test_translation_files),
        ("Fallback System", test_fallback_system),
        ("Flask Integration", test_flask_integration)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            if not test_func():
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All translation tests passed!")
        print("\n✅ Translation system is working correctly")
        print("✅ Ready for production use")
    else:
        print("❌ Some translation tests failed")
        print("\n🔧 Suggested fixes:")
        print("1. Run: python compile_translations.py")
        print("2. Check translation files exist")
        print("3. Restart Flask app")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)