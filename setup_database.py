#!/usr/bin/env python
"""Check and create database if needed"""

import pyodbc

# Connect to SQL Server
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost;'
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
)
cursor = conn.cursor()

# Check if database exists
cursor.execute("SELECT name FROM sys.databases WHERE name='AI_Delivery_Advisor'")
db = cursor.fetchone()

if db:
    print('✅ Database AI_Delivery_Advisor exists')
else:
    print('❌ Database AI_Delivery_Advisor does NOT exist')
    print('Creating database...')
    cursor.execute('CREATE DATABASE [AI_Delivery_Advisor]')
    conn.commit()
    print('✅ Database created successfully')

conn.close()
