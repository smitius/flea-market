# 📁 Translation Files Reference

This document explains all translation-related files in the repository.

## 🔧 Developer Tools (Keep These)

### Core Translation Scripts
- **`extract_translations.py`** - Extracts translatable strings from code
- **`compile_translations.py`** - Compiles .po files to .mo files
- **`create_safe_translations.py`** - Fallback compilation method
- **`test_translations.py`** - Tests translation system functionality

### Configuration Files
- **`babel.cfg`** - Babel configuration for string extraction
- **`app/translations_fallback.py`** - Emergency fallback translations

### Documentation
- **`TRANSLATION_GUIDE.md`** - Quick developer reference
- **`TRANSLATION_FILES.md`** - This file (file reference)

## 📚 Translation Data Files (Keep These)

### Swedish Translations
- **`app/translations/sv/LC_MESSAGES/messages.po`** - Human-readable Swedish translations
- **`app/translations/sv/LC_MESSAGES/messages.mo`** - Compiled Swedish translations

### English Translations  
- **`app/translations/en/LC_MESSAGES/messages.po`** - Human-readable English translations
- **`app/translations/en/LC_MESSAGES/messages.mo`** - Compiled English translations

## 🗑️ Files Removed (One-time Use)

These files were used during initial setup and are no longer needed:

- ~~`setup_multilanguage.py`~~ - One-time setup script
- ~~`migrate_add_language_support.py`~~ - Database migration (already run)
- ~~`test_multilanguage.py`~~ - Development testing
- ~~`test_translations_simple.py`~~ - Encoding fix testing
- ~~`IMPLEMENTATION_SUMMARY.md`~~ - Development notes
- ~~`ENCODING_FIX_SUMMARY.md`~~ - Development notes
- ~~`MULTILANGUAGE_README.md`~~ - Merged into main README
- ~~`manual_compile_translations.py`~~ - Replaced by better version
- ~~`requirements_babel.txt`~~ - Merged into main requirements.txt

## 🎯 File Purposes

| File | Purpose | When to Use |
|------|---------|-------------|
| `extract_translations.py` | Find new translatable strings | After adding `_('text')` to code |
| `compile_translations.py` | Convert .po to .mo files | After editing translations |
| `create_safe_translations.py` | Fallback compilation | If pybabel fails |
| `test_translations.py` | Verify system works | After translation changes |
| `*.po files` | Edit translations | When adding/changing translations |
| `*.mo files` | Used by Flask | Auto-generated, don't edit |

## 🔄 Typical Workflow

1. **Add translatable text**: `{{ _('New Text') }}` in templates
2. **Extract strings**: `python extract_translations.py`
3. **Edit translations**: Modify `.po` files
4. **Compile**: `python compile_translations.py`
5. **Test**: `python test_translations.py`
6. **Restart app**: See changes in browser

## 📦 Repository Size Impact

**Translation files total**: ~50KB
- Documentation: ~15KB
- Scripts: ~20KB  
- Translation data: ~15KB

**Clean repository**: Removed ~200KB of temporary development files.

---

**Note**: All kept files serve ongoing development and maintenance purposes.