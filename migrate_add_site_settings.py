#!/usr/bin/env python3
"""
Migration script to add SiteSettings table and populate with default values
Run this script once to update your existing database
"""

import sqlite3
import os
from dotenv import load_dotenv

def migrate_database():
    load_dotenv()
    
    # Get database path
    db_path = os.path.join('instance', 'flea_market.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        print("If this is a new installation, just run 'python init_db.py' instead")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if site_settings table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='site_settings'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("site_settings table already exists. No migration needed.")
            return
        
        # Create the site_settings table
        cursor.execute('''
            CREATE TABLE site_settings (
                id INTEGER PRIMARY KEY,
                site_name VARCHAR(100) NOT NULL DEFAULT 'Vår egen Loppis',
                welcome_message VARCHAR(200) NOT NULL DEFAULT 'Hej och Välkommen',
                general_info TEXT NOT NULL DEFAULT 'Vi rensar ut några saker vi inte längre behöver – och det kan vara precis vad du letar efter.',
                contact_info TEXT NOT NULL DEFAULT 'Kontakta oss för mer information.',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Get values from environment variables if they exist
        site_name = os.getenv('SITE_NAME', 'Vår egen Loppis')
        whatsapp = os.getenv('WHATSAPP_NUMBER', '')
        address = os.getenv('APARTMENT_ADDRESS', '')
        
        # Create contact info from env variables
        contact_parts = []
        if whatsapp:
            contact_parts.append(f"Telefon/WhatsApp: {whatsapp}")
        if address:
            contact_parts.append(f"Adress: {address}")
        if site_name and site_name != 'Vår egen Loppis':
            contact_parts.append(f"Kontakt: {site_name}")
        
        contact_info = '\n'.join(contact_parts) if contact_parts else 'Kontakta oss för mer information.'
        
        # Insert default settings
        cursor.execute('''
            INSERT INTO site_settings (site_name, welcome_message, general_info, contact_info)
            VALUES (?, ?, ?, ?)
        ''', (
            'Vår egen Loppis',
            'Hej och Välkommen',
            'Vi rensar ut några saker vi inte längre behöver – och det kan vara precis vad du letar efter. Från användbara vardagssaker till saker som kan ge lite extra glädje, hoppas vi att du hittar något här som passar dig. Ta en titt och hör gärna av dig om något fångar ditt öga!',
            contact_info
        ))
        
        conn.commit()
        print("Successfully created site_settings table with default values")
        print("You can now edit these settings from the admin panel")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()