import sys
import os

print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")
print(f"IS_WINDOWS: {sys.platform.startswith('win')}")
print()

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("Environment:")
print(f"  DB_SERVER: '{os.getenv('DB_SERVER')}'")
print(f"  DB_USER: '{os.getenv('DB_USER', '')}'")
print(f"  DB_PASSWORD: '{os.getenv('DB_PASSWORD', '')}'")
print()

# Try to trace the get_connection
print("Calling get_connection...")
try:
    from database import get_connection
    conn = get_connection()
    print("✅ Success!")
    conn.close()
except Exception as e:
    print(f"❌ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
