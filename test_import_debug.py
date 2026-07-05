import os
import sys

# Load .env first
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("=" * 70)
print("DEBUG: Before importing database module")
print("=" * 70)
print(f"DB_USER from env: '{os.getenv('DB_USER')}'")
print(f"DB_PASSWORD from env: '{os.getenv('DB_PASSWORD')}'")
print()

# Now import the module
sys.path.insert(0, os.getcwd())
from database import get_connection

print("=" * 70)
print("DEBUG: Inside get_connection logic")
print("=" * 70)

# Manually run the logic
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

print(f"username: '{username}' (type: {type(username).__name__})")
print(f"password: '{password}' (type: {type(password).__name__})")
print(f"bool(username): {bool(username)}")
print(f"bool(password): {bool(password)}")
print(f"username and password: {username and password}")
print()

# Try connection
print("=" * 70)
print("Attempting connection...")
print("=" * 70)

try:
    conn = get_connection()
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
