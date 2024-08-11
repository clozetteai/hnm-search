import sqlite3
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
        
        # table_name = os.path.splitext(os.path.basename(csv_file_path))[0]
        
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
    
def load_sqlite_db(sqlite_db_path):
    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()
    
    return cursor

def get_db_columns(cursor):

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    db_schema = {}

    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        column_info = {col[1]: col[2] for col in columns}
        db_schema[table_name] = column_info

    return db_schema