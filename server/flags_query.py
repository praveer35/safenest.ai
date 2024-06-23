import sqlite3
from datetime import datetime

def input_flag(classification, description):
    # Get the current system datetime
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Connect to SQLite database
    conn = sqlite3.connect('flags.db')
    cursor = conn.cursor()

    # Insert a new record into the Flags table
    cursor.execute('''
    INSERT INTO Flags (Classification, Description, Timestamp)
    VALUES (?, ?, ?)
    ''', (classification, description, timestamp))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


def insert_flag_table(flag_id, flag_type, session_id, time_seconds, description):
    # Connect to the SQLite database
    conn = sqlite3.connect('flags.db')
    cursor = conn.cursor()
    
    # SQL command to insert a new row into FlagTable
    sql = '''
    INSERT INTO FlagTable (flag_id, type, session_id, time, description)
    VALUES (?, ?, ?, ?, ?)
    '''
    
    # Execute the SQL command with the provided parameters
    cursor.execute(sql, (flag_id, flag_type, session_id, time_seconds, description))
    
    # Commit the transaction
    conn.commit()
    
    # Close the connection
    conn.close()

def get_top_3_flag_types(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQL command to get the 3 most common flag types
    sql = '''
    SELECT type, COUNT(*) as count
    FROM FlagTable
    GROUP BY type
    ORDER BY count DESC
    LIMIT 3
    '''
    
    # Execute the SQL command
    cursor.execute(sql)
    
    # Fetch the results
    top_3_flag_types = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return top_3_flag_types