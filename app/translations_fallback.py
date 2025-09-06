"""
Fallback translation system for when Flask-Babel has issues
"""

TRANSLATIONS = {
    'sv': {
        'Dashboard': 'Instrumentpanel',
        'Logout': 'Logga ut',
        'Admin': 'Admin',
        'Contact': 'Kontakt',
        'Price': 'Pris',
        'Sold': 'Sald',
        'More Pictures': 'Fler Bilder',
        'Admin Dashboard': 'Admin Instrumentpanel',
        'Add New Item': 'Lagg till ny vara',
        'Sort by': 'Sortera efter',
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
    },
    'en': {
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
}

def get_translation(text, language='sv'):
    """Get translation for text in specified language"""
    if language in TRANSLATIONS and text in TRANSLATIONS[language]:
        return TRANSLATIONS[language][text]
    return text  # Return original text if no translation found