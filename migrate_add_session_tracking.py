#!/usr/bin/env python3
"""
Migration script to add UserSession table for session tracking
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
        
        # Check if user_session table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_session'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("user_session table already exists. No migration needed.")
            return
        
        # Create the user_session table
        cursor.execute('''
            CREATE TABLE user_session (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                session_id VARCHAR(255) NOT NULL UNIQUE,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES user (id)
            )
        ''')
        
        # Create index for better performance
        cursor.execute('CREATE INDEX idx_user_session_user_id ON user_session(user_id)')
        cursor.execute('CREATE INDEX idx_user_session_active ON user_session(is_active)')
        
        conn.commit()
        print("Successfully created user_session table with indexes")
        print("Session tracking is now enabled!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()