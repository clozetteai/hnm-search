import sqlite3
import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
import csv
import os

def csv_to_sqlite(csv_file_path, sqlite_db_path, table_name):
    """
    Convert a CSV file to an SQLite database.
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
    
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    with open(csv_file_path, 'r', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        columns = reader.fieldnames
        if not columns:
            raise ValueError("No columns found in the CSV file")
        
        create_table_query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                {", ".join([f'"{col}" TEXT' for col in columns])}
            )
        '''
        cursor.execute(create_table_query)
        
        for row in reader:
            columns_str = ', '.join(f'"{col}"' for col in columns)
            placeholders = ', '.join(f':{col}' for col in columns)
            insert_query = f'''
                INSERT INTO {table_name} ({columns_str})
                VALUES ({placeholders})
            '''
            cursor.execute(insert_query, row)
    
    conn.commit()
    conn.close()
    print(f"Data from {csv_file_path} has been successfully saved to {sqlite_db_path}")
    
def get_tidb_cursor(config):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    return cursor