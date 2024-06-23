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

def get_description_by_flag_id(flag_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('flags.db')
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



def add_user(username, password, email):
    # Connect to the SQLite database
    conn = sqlite3.connect('flags.db')
    cursor = conn.cursor()
    
    # SQL command to insert a new row into FlagTable
    sql = '''
    INSERT INTO LoginTable (username, password, email)
    VALUES (?, ?, ?)
    '''
    
    # Execute the SQL command with the provided parameters
    cursor.execute(sql, (username, password, email))
    
    # Commit the transaction
    conn.commit()
    
    # Close the connection
    conn.close()


def is_user(username, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('flags.db')
    cursor = conn.cursor()
    
    # SQL command to insert a new row into FlagTable
    sql = '''
    SELECT * FROM LoginTable WHERE username=? AND password=?
    '''
    
    # Execute the SQL command with the provided parameters
    cursor.execute(sql, (username, password))
    
    # Commit the transaction
    result = cursor.fetchall()
    print(result)
    
    # Close the connection
    conn.close()

    return len(result) > 0

def add_session(vitals_str, ai_data_str, bpm_flags_str, temp_flags_str, choking_flags_str, shocking_flags_str, suffocation_flags_str, sharp_flags_str):
    conn = sqlite3.connect('flags.db')
    cursor = conn.cursor()

    sql = '''INSERT INTO SessionTable (vitals_str, ai_data_str, bpm_flags_str, temp_flags_str, choking_flags_str, shocking_flags_str, suffocation_flags_str, sharp_flags_str)
            VALUES (?,?,??,?,?,?,?)'''
    
    cursor.execute(sql, (vitals_str, ai_data_str, bpm_flags_str, temp_flags_str, choking_flags_str, shocking_flags_str, suffocation_flags_str, sharp_flags_str))
    conn.commit()
    conn.close()