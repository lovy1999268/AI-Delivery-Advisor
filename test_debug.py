import os
import sys

print("=" * 70)
print("DEBUG: Checking .env loading")
print("=" * 70)

# Check if .env exists
env_path = '.env'
print(f"Current directory: {os.getcwd()}")
print(f".env exists: {os.path.exists(env_path)}")

# Try loading .env
try:
    from dotenv import load_dotenv
    result = load_dotenv(env_path, override=True)
    print(f"load_dotenv result: {result}")
except ImportError:
    print("dotenv not available")

# Check environment variables
print("\nEnvironment variables:")
print(f"DB_SERVER = {os.getenv('DB_SERVER', 'NOT SET')}")
print(f"DB_NAME = {os.getenv('DB_NAME', 'NOT SET')}")
print(f"DB_USER = {os.getenv('DB_USER', 'NOT SET')}")
print(f"DB_PASSWORD = {os.getenv('DB_PASSWORD', 'NOT SET')}")

print("\n" + "=" * 70)
print("Now testing database connection...")
print("=" * 70 + "\n")

# Now test connection
sys.path.insert(0, os.getcwd())
from database import get_connection

try:
    conn = get_connection()
    print('✅ Connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Error: {e}')
