#!/usr/bin/env python
"""
SQL Server Connection Diagnostic Script
Tests database connectivity and provides troubleshooting info
"""

import os
import sys

# Try to load .env, but don't fail if dotenv isn't installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_SERVER = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
DB_NAME = os.getenv("DB_NAME", "AI_Delivery_Advisor")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print("=" * 70)
print("SQL SERVER CONNECTION DIAGNOSTIC")
print("=" * 70)
print()

print("📋 Configuration:")
print(f"   Server:   {DB_SERVER}")
print(f"   Database: {DB_NAME}")
print(f"   Auth:     {'SQL Authentication' if DB_USER else 'Windows Authentication'}")
print()

# Test 1: Check if pyodbc is installed
print("Test 1: Check pyodbc installation...")
try:
    import pyodbc
    print("   ✅ pyodbc is installed")
except ImportError:
    print("   ❌ pyodbc not installed")
    print("   Install with: python -m pip install pyodbc")
    sys.exit(1)

print()

# Test 2: List available ODBC drivers
print("Test 2: Check ODBC drivers...")
try:
    drivers = pyodbc.drivers()
    print(f"   Available drivers: {len(drivers)}")
    for driver in drivers:
        print(f"     - {driver}")
    
    if any("SQL Server" in d for d in drivers):
        print("   ✅ SQL Server ODBC driver found")
    else:
        print("   ⚠️  No SQL Server ODBC driver found")
        print("   Install from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
except Exception as e:
    print(f"   ❌ Error listing drivers: {e}")

print()

# Test 3: Try to connect
print("Test 3: Test database connection...")
try:
    if DB_USER and DB_PASSWORD:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
            f"TrustServerCertificate=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )
    
    print(f"   Connection string: {conn_str[:80]}...")
    conn = pyodbc.connect(conn_str, timeout=3)
    print("   ✅ Connection successful!")
    conn.close()
    
except pyodbc.DatabaseError as e:
    print(f"   ❌ Connection failed: {e}")
    print()
    print("   Possible solutions:")
    print("   1. Check SQL Server is running (Services > SQL Server)")
    print("   2. Verify server name in .env (try 'localhost', '(local)', or '127.0.0.1')")
    print("   3. Try this in PowerShell: sqlcmd -S localhost\\SQLEXPRESS -E")
    print("   4. For Azure SQL: Use 'server.database.windows.net' format")
    
except Exception as e:
    print(f"   ❌ Unexpected error: {type(e).__name__}: {e}")

print()
print("=" * 70)
print("Need help? Check the troubleshooting section in README.md")
print("=" * 70)

DB_SERVER = os.getenv("DB_SERVER", "localhost\\SQLEXPRESS")
DB_NAME = os.getenv("DB_NAME", "AI_Delivery_Advisor")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

print("=" * 70)
print("SQL SERVER CONNECTION DIAGNOSTIC")
print("=" * 70)
print()

print("📋 Configuration:")
print(f"   Server:   {DB_SERVER}")
print(f"   Database: {DB_NAME}")
print(f"   Auth:     {'SQL Authentication' if DB_USER else 'Windows Authentication'}")
print()

# Test 1: Check if pyodbc is installed
print("Test 1: Check pyodbc installation...")
try:
    import pyodbc
    print("   ✅ pyodbc is installed")
    print(f"   Version: {pyodbc.__version__}")
except ImportError:
    print("   ❌ pyodbc not installed")
    print("   Install with: pip install pyodbc")
    sys.exit(1)

print()

# Test 2: List available ODBC drivers
print("Test 2: Check ODBC drivers...")
try:
    drivers = pyodbc.drivers()
    print(f"   Available drivers: {len(drivers)}")
    for driver in drivers:
        print(f"     - {driver}")
    
    if any("SQL Server" in d for d in drivers):
        print("   ✅ SQL Server ODBC driver found")
    else:
        print("   ⚠️  No SQL Server ODBC driver found")
        print("   Install from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
except Exception as e:
    print(f"   ❌ Error listing drivers: {e}")

print()

# Test 3: Try to connect
print("Test 3: Test database connection...")
try:
    if DB_USER and DB_PASSWORD:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
            f"TrustServerCertificate=yes;"
        )
    else:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate=yes;"
        )
    
    print(f"   Connection string: {conn_str[:80]}...")
    conn = pyodbc.connect(conn_str, timeout=3)
    print("   ✅ Connection successful!")
    conn.close()
    
except pyodbc.DatabaseError as e:
    print(f"   ❌ Connection failed: {e}")
    print()
    print("   Possible solutions:")
    print("   1. Check SQL Server is running (Services > SQL Server)")
    print("   2. Verify server name in .env (try 'localhost', '(local)', or '127.0.0.1')")
    print("   3. Try this: sqlcmd -S localhost\\SQLEXPRESS -E")
    print("   4. For Azure SQL: Use 'server.database.windows.net' format")
    
except Exception as e:
    print(f"   ❌ Unexpected error: {type(e).__name__}: {e}")

print()
print("=" * 70)
print("Need help? Check the troubleshooting section in README.md")
print("=" * 70)
