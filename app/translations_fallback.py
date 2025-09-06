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
        'Delete this item?': 'Ta bort denna vara?',
        # Search and Sort
        'Search items...': 'Sok varor...',
        'Clear search': 'Rensa sokning',
        'Sort by': 'Sortera efter',
        'Newest first': 'Nyaste forst',
        'Oldest first': 'Aldsta forst',
        'Price: Low to High': 'Pris: Lag till hog',
        'Price: High to Low': 'Pris: Hog till lag',
        'Name A-Z': 'Namn A-O',
        'Most Popular': 'Mest populara',
        'items found for': 'varor hittade for',
        'No items found': 'Inga varor hittades',
        'No items match your search for': 'Inga varor matchar din sokning efter',
        'Show all items': 'Visa alla varor',
        'No items available': 'Inga varor tillgangliga',
        'There are currently no items for sale.': 'Det finns for narvarande inga varor till salu.'
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
        'Delete this item?': 'Delete this item?',
        # Search and Sort
        'Search items...': 'Search items...',
        'Clear search': 'Clear search',
        'Sort by': 'Sort by',
        'Newest first': 'Newest first',
        'Oldest first': 'Oldest first',
        'Price: Low to High': 'Price: Low to High',
        'Price: High to Low': 'Price: High to Low',
        'Name A-Z': 'Name A-Z',
        'Most Popular': 'Most Popular',
        'items found for': 'items found for',
        'No items found': 'No items found',
        'No items match your search for': 'No items match your search for',
        'Show all items': 'Show all items',
        'No items available': 'No items available',
        'There are currently no items for sale.': 'There are currently no items for sale.'
    }
}

def get_translation(text, language='sv'):
    """Get translation for text in specified language"""
    if language in TRANSLATIONS and text in TRANSLATIONS[language]:
        return TRANSLATIONS[language][text]
    return text  # Return original text if no translation found