import sqlite3

def query_sensor_data():
    # Connect to the database
    conn = sqlite3.connect('program_453_database.db')
    cursor = conn.cursor()
    
    # Get user inputs
    device_id = input("Enter device_id: ")
    start_timestamp = input("Enter start timestamp (YYYY-MM-DD HH:MM:SS): ")
    end_timestamp = input("Enter end timestamp (YYYY-MM-DD HH:MM:SS): ")
    sort_column = input("Enter sort column (temperature, humidity, timestamp): ")
    sort_direction = input("Enter sort direction (ASC, DESC): ")
    
    # Construct the SQL query
    query = f"""
    SELECT device_id, timestamp, temperature, humidity
    FROM sensor_data
    WHERE device_id = ? AND timestamp BETWEEN ? AND ?
    ORDER BY {sort_column} {sort_direction}
    """
    
    # Execute the query
    cursor.execute(query, (device_id, start_timestamp, end_timestamp))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Call the function
query_sensor_data()