import sqlite3

def query_sensor_data(device_id, start_timestamp, end_timestamp, sort_column, sort_direction):
    # Connect to the database
    conn = sqlite3.connect('program_453_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT device_id, timestamp, temperature, humidity FROM sensor_data WHERE device_id = ? AND timestamp BETWEEN ? AND ? ORDER BY {sort_column} {sort_direction}"
    
    # Execute the query
    cursor.execute(query, (device_id, start_timestamp, end_timestamp))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Example usage
query_sensor_data('sensor_1', '2023-10-01 09:30:00', '2023-10-01 10:30:00', 'temperature', 'DESC')
query_sensor_data('sensor_7', '2023-10-01 15:00:00', '2023-10-01 17:00:00', 'temperature', 'ASC')