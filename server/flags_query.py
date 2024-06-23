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
    INSERT INTO FlagsTable (Classification, Description, Timestamp)
    VALUES (?, ?, ?)
    ''', (classification, description, timestamp))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def get_description_by_flag_id(db_path, flag_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # SQL command to get the description based on flag_id
    sql = '''
    SELECT description
    FROM FlagsTable
    WHERE flag_id = ?
    '''
    
    # Execute the SQL command with the provided flag_id
    cursor.execute(sql, (flag_id,))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # Return the description if found, otherwise return None
    return result[0] if result else None

def insert_flag_table(flag_id, flag_type, session_id, time_seconds, description):
    # Connect to the SQLite database
    conn = sqlite3.connect('flags.db')
    cursor = conn.cursor()
    
    # SQL command to insert a new row into FlagTable
    sql = '''
    INSERT INTO FlagsTable (flag_id, type, session_id, time, description)
    VALUES (?, ?, ?, ?, ?)
    '''
    
    # Execute the SQL command with the provided parameters
    cursor.execute(sql, (flag_id, flag_type, session_id, time_seconds, description))
    
    # Commit the transaction
    conn.commit()
    
    # Close the connection
    conn.close()



def get_top_3_flag_types():
    # Connect to the SQLite database
    conn = sqlite3.connect('flags.db')
    cursor = conn.cursor()
    
    # SQL command to get the 3 most common flag types
    sql = '''
    SELECT type, COUNT(*) as count
    FROM FlagsTable
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