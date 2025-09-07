#!/usr/bin/env python3
"""
Create safe translation files without encoding issues
"""

import os
import struct

def create_simple_mo_file(translations, output_path):
    """Create a simple .mo file from translations dictionary"""
    
    # Prepare data
    keys = sorted(translations.keys())
    values = [translations[key] for key in keys]
    
    # Encode strings
    kencoded = [key.encode('utf-8') for key in keys]
    vencoded = [value.encode('utf-8') for value in values]
    
    # Calculate offsets
    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + sum(len(k) + 1 for k in kencoded)
    
    koffsets = []
    voffsets = []
    
    # Key offsets
    offset = keystart
    for k in kencoded:
        koffsets.append(offset)
        offset += len(k) + 1
    
    # Value offsets  
    offset = valuestart
    for v in vencoded:
        voffsets.append(offset)
        offset += len(v) + 1
    
    # Write .mo file
    with open(output_path, 'wb') as f:
        # Magic number
        f.write(struct.pack('<I', 0x950412de))
        # Version
        f.write(struct.pack('<I', 0))
        # Number of entries
        f.write(struct.pack('<I', len(keys)))
        # Offset of key table
        f.write(struct.pack('<I', 7 * 4))
        # Offset of value table
        f.write(struct.pack('<I', 7 * 4 + 8 * len(keys)))
        # Hash table size (unused)
        f.write(struct.pack('<I', 0))
        # Hash table offset (unused)
        f.write(struct.pack('<I', 0))
        
        # Key table
        for i, key in enumerate(keys):
            f.write(struct.pack('<I', len(kencoded[i])))
            f.write(struct.pack('<I', koffsets[i]))
        
        # Value table
        for i, key in enumerate(keys):
            f.write(struct.pack('<I', len(vencoded[i])))
            f.write(struct.pack('<I', voffsets[i]))
        
        # Keys
        for k in kencoded:
            f.write(k)
            f.write(b'\x00')
        
        # Values
        for v in vencoded:
            f.write(v)
            f.write(b'\x00')

def create_safe_translations():
    """Create safe translation files for all supported languages"""
    
    # Swedish translations (without problematic characters)
    swedish_translations = {
        'Dashboard': 'Instrumentpanel',
        'Logout': 'Logga ut',
        'Admin': 'Admin',
        'Contact': 'Kontakt',
        'Price': 'Pris',
        'Sold': 'Sald',
        'More Pictures': 'Fler Bilder',
        'Admin Dashboard': 'Admin Instrumentpanel',
        'Add New Item': 'Lagg till ny vara',
        'Sort by': 'Sortering',
        'Date Created': 'Skapad datum',
        'Most Viewed': 'Mest visade',
        'Name': 'Namn',
        'Views': 'Visningar',
        'Actions': 'Atgarder',
        'Edit': 'Redigera',
        'Delete': 'Ta bort',
        'Yes': 'Ja',
        'No': 'Nej',
        'Delete this item?': 'Ta bort denna vara?'
    }
    
    # English translations
    english_translations = {
        'Dashboard': 'Dashboard',
        'Logout': 'Logout',
        'Admin': 'Admin',
        'Contact': 'Contact',
        'Price': 'Price',
        'Sold': 'Sold',
        'More Pictures': 'More Pictures',
        'Admin Dashboard': 'Admin Dashboard',
        'Add New Item': 'Add New Item',
        'Sort by': 'Sort by',
        'Date Created': 'Date Created',
        'Most Viewed': 'Most Viewed',
        'Name': 'Name',
        'Views': 'Views',
        'Actions': 'Actions',
        'Edit': 'Edit',
        'Delete': 'Delete',
        'Yes': 'Yes',
        'No': 'No',
        'Delete this item?': 'Delete this item?'
    }
    
    # Slovak translations
    slovak_translations = {
        'Dashboard': 'Nástenka',
        'Logout': 'Odhlásiť sa',
        'Admin': 'Admin',
        'Contact': 'Kontakt',
        'Price': 'Cena',
        'Sold': 'Predané',
        'More Pictures': 'Viac obrázkov',
        'Admin Dashboard': 'Administrácia',
        'Add New Item': 'Pridať novú položku',
        'Sort by': 'Zoradiť podľa',
        'Date Created': 'Dátum vytvorenia',
        'Most Viewed': 'Najprezeranejšie',
        'Name': 'Názov',
        'Views': 'Zobrazenia',
        'Actions': 'Akcie',
        'Edit': 'Upraviť',
        'Delete': 'Vymazať',
        'Yes': 'Áno',
        'No': 'Nie',
        'Delete this item?': 'Vymazať túto položku?'
    }
    
    # Czech translations
    czech_translations = {
        'Dashboard': 'Nástěnka',
        'Logout': 'Odhlásit se',
        'Admin': 'Admin',
        'Contact': 'Kontakt',
        'Price': 'Cena',
        'Sold': 'Prodáno',
        'More Pictures': 'Více obrázků',
        'Admin Dashboard': 'Administrace',
        'Add New Item': 'Přidat novou položku',
        'Sort by': 'Seřadit podle',
        'Date Created': 'Datum vytvoření',
        'Most Viewed': 'Nejprohlíženější',
        'Name': 'Název',
        'Views': 'Zobrazení',
        'Actions': 'Akce',
        'Edit': 'Upravit',
        'Delete': 'Smazat',
        'Yes': 'Ano',
        'No': 'Ne',
        'Delete this item?': 'Smazat tuto položku?'
    }
    
    # Create directories if they don't exist
    os.makedirs('app/translations/sv/LC_MESSAGES', exist_ok=True)
    os.makedirs('app/translations/en/LC_MESSAGES', exist_ok=True)
    os.makedirs('app/translations/sk/LC_MESSAGES', exist_ok=True)
    os.makedirs('app/translations/cs/LC_MESSAGES', exist_ok=True)
    
    # Create .mo files for all languages
    print("🔨 Creating Swedish translations...")
    create_simple_mo_file(swedish_translations, 'app/translations/sv/LC_MESSAGES/messages.mo')
    
    print("🔨 Creating English translations...")
    create_simple_mo_file(english_translations, 'app/translations/en/LC_MESSAGES/messages.mo')
    
    print("🔨 Creating Slovak translations...")
    create_simple_mo_file(slovak_translations, 'app/translations/sk/LC_MESSAGES/messages.mo')
    
    print("🔨 Creating Czech translations...")
    create_simple_mo_file(czech_translations, 'app/translations/cs/LC_MESSAGES/messages.mo')
    
    print("✅ Safe translation files created for all languages!")
    print("🚀 You can now restart your Flask app")

if __name__ == '__main__':
    create_safe_translations()