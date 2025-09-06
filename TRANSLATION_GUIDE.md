# 🌍 Translation Developer Guide

Quick reference for developers working with translations in the Flea Market App.

## 🚀 Quick Commands

```bash
# Extract new translatable strings from code
python extract_translations.py

# Compile translation files after editing
python compile_translations.py

# Create safe translations (fallback method)
python create_safe_translations.py
```

## 📝 Adding New Translatable Text

### 1. In Templates (.html files)
```html
<!-- Before -->
<button>Save Changes</button>

<!-- After -->
<button>{{ _('Save Changes') }}</button>
```

### 2. In Python Code
```python
from flask_babel import gettext as _

# In routes
flash(_('Settings updated successfully'), 'success')

# In forms
label = _('Enter your name')
```

### 3. Update Translations
```bash
# 1. Extract new strings
python extract_translations.py

# 2. Edit translation files
# app/translations/sv/LC_MESSAGES/messages.po
# app/translations/en/LC_MESSAGES/messages.po

# 3. Compile translations
python compile_translations.py

# 4. Restart Flask app
```

## 🔧 Translation File Format

**messages.po structure:**
```po
msgid "English text"
msgstr "Translated text"

msgid "Save Changes"
msgstr "Spara ändringar"  # Swedish

msgid "Delete this item?"
msgstr "Ta bort denna vara?"
```

## 🌐 Currently Translated Elements

| English | Swedish | Context |
|---------|---------|---------|
| Dashboard | Instrumentpanel | Navigation |
| Contact | Kontakt | Main page |
| Price | Pris | Item display |
| Sold | Sald | Item status |
| Add New Item | Lagg till ny vara | Admin button |
| Edit | Redigera | Admin action |
| Delete | Ta bort | Admin action |

## 🛠 File Structure

```
Translation Files:
├── babel.cfg                           # Babel configuration
├── extract_translations.py             # Extract strings from code
├── compile_translations.py             # Compile .po to .mo files
├── create_safe_translations.py         # Fallback compilation
├── app/translations_fallback.py        # Emergency fallback
└── app/translations/
    ├── sv/LC_MESSAGES/
    │   ├── messages.po                 # Swedish (editable)
    │   └── messages.mo                 # Swedish (compiled)
    └── en/LC_MESSAGES/
        ├── messages.po                 # English (editable)
        └── messages.mo                 # English (compiled)
```

## 🎯 Best Practices

1. **Keep strings short and clear**
2. **Use context comments in .po files**
3. **Test both languages after changes**
4. **Avoid hardcoded text in templates**
5. **Use ASCII-safe characters for Swedish** (å→a, ä→a, ö→o)

## 🚨 Troubleshooting

**Problem**: Translations not showing
**Solution**: 
```bash
python compile_translations.py
# Restart Flask app
```

**Problem**: New strings not extracted
**Solution**:
```bash
python extract_translations.py
# Edit .po files
python compile_translations.py
```

**Problem**: Encoding errors
**Solution**: Use `create_safe_translations.py` or check `app/translations_fallback.py`

---

**Quick tip**: Always test both Swedish and English after making translation changes!