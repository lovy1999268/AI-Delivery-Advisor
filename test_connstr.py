import os
import sys

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Get values
server = os.getenv("DB_SERVER", "localhost")
database = os.getenv("DB_NAME", "AI_Delivery_Advisor")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

print("=" * 70)
print("DEBUG: Connection String Builder")
print("=" * 70)
print(f"DB_SERVER: '{server}'")
print(f"DB_NAME: '{database}'")
print(f"DB_USER: '{username}' (len={len(username) if username else 0})")
print(f"DB_PASSWORD: '{password}' (len={len(password) if password else 0})")
print()

if username and password:
    print("Path: SQL Authentication")
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"TrustServerCertificate=yes;"
    )
else:
    print("Path: Windows Authentication")
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )

print(f"Connection String:\n{conn_str}")
print()

# Try connecting
print("=" * 70)
print("Testing connection...")
print("=" * 70)

import pyodbc
try:
    conn = pyodbc.connect(conn_str)
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
