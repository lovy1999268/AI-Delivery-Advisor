#!/usr/bin/env python3
from database import get_connection, init_database

try:
    init_database()
    conn = get_connection()
    
    # Test connection
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("✅ SQLite connection successful!")
    print(f"Database tables: {[t[0] for t in tables]}")
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
