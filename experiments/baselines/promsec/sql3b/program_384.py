import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_384_database.db')
cursor = conn.cursor()

# Prompt user for input
min_temp = float(input("Enter minimum temperature: "))
max_temp = float(input("Enter maximum temperature: "))
location = input("Enter location: ")
status = input("Enter status: ")

# Adjust the temperature range
adjusted_min_temp = min_temp + 0.5
adjusted_max_temp = max_temp + 0.5

# Construct the SQL query
query = f"""
SELECT device_id, name, status, temperature, location
FROM devices
WHERE (temperature BETWEEN {adjusted_min_temp} AND {adjusted_max_temp})
   OR (location = '{location}')
   AND (status = '{status}')
"""

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()