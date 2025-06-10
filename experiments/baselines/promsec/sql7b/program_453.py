import sqlite3

# Connect to the database
conn = sqlite3.connect('program_453_database.db')
cursor = conn.cursor()

# Get user inputs
device_id = input("Enter device_id: ")
start_timestamp = input("Enter start_timestamp: ")
end_timestamp = input("Enter end_timestamp: ")
sort_column = input("Enter column to sort by (temperature, humidity, timestamp): ")
sort_direction = input("Enter sort direction (ASC, DESC): ")

# Construct the SQL query
query = f"SELECT * FROM sensor_data WHERE device_id = ? AND timestamp BETWEEN ? AND ? ORDER BY {sort_column} {sort_direction}"

# Execute the query
cursor.execute(query, (device_id, start_timestamp, end_timestamp))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()