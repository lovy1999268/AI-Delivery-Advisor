import sys
sys.path.insert(0, 'C:/Users/dines/OneDrive/Desktop/AI-Delivery-Advisor')

from database import get_connection

try:
    conn = get_connection()
    print('✅ Connection successful from database module!')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM sys.tables')
    count = cursor.fetchone()[0]
    print(f'✅ Database is accessible, contains {count} tables')
    conn.close()
except Exception as e:
    print(f'❌ Error: {type(e).__name__}: {e}')
