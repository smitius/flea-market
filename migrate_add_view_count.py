#!/usr/bin/env python3
"""
Migration script to add view_count column to existing Item table
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
        
        # Check if view_count column already exists
        cursor.execute("PRAGMA table_info(item)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'view_count' in columns:
            print("view_count column already exists. No migration needed.")
            return
        
        # Add the view_count column with default value 0
        cursor.execute("ALTER TABLE item ADD COLUMN view_count INTEGER DEFAULT 0")
        
        # Update all existing items to have view_count = 0
        cursor.execute("UPDATE item SET view_count = 0 WHERE view_count IS NULL")
        
        conn.commit()
        print("Successfully added view_count column to Item table")
        print("All existing items now have view_count = 0")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()