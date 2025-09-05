#!/usr/bin/env python3
"""
Migration script to add FailedLoginAttempt table for security features
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
        
        # Check if failed_login_attempt table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='failed_login_attempt'")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("failed_login_attempt table already exists. No migration needed.")
            return
        
        # Create the failed_login_attempt table
        cursor.execute('''
            CREATE TABLE failed_login_attempt (
                id INTEGER PRIMARY KEY,
                ip_address VARCHAR(45) NOT NULL,
                username VARCHAR(80),
                user_agent TEXT,
                attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX idx_failed_login_ip ON failed_login_attempt(ip_address)')
        cursor.execute('CREATE INDEX idx_failed_login_time ON failed_login_attempt(attempted_at)')
        
        conn.commit()
        print("Successfully created failed_login_attempt table with indexes")
        print("Security features are now enabled!")
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()