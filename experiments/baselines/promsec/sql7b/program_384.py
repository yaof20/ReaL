import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_384_database.db')
cursor = conn.cursor()

# Prompt user for inputs
min_temp = float(input("Enter minimum temperature: "))
max_temp = float(input("Enter maximum temperature: "))
location = input("Enter location: ")
status = input("Enter device status: ")

# Adjust temperature range
min_temp += 0.5
max_temp += 0.5

# Construct SQL query
query = """
SELECT * FROM devices
WHERE (temperature BETWEEN ? AND ?) OR location = ? AND status = ?
"""

# Execute the query
cursor.execute(query, (min_temp, max_temp, location, status))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()