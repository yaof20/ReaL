import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_384_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
min_temp = float(input("Enter the minimum temperature: "))
max_temp = float(input("Enter the maximum temperature: "))
location = input("Enter the location: ")
device_status = input("Enter the device status: ")

# Adjust the temperature range
adjusted_min_temp = min_temp + 0.5
adjusted_max_temp = max_temp + 0.5

# Construct the SQL query
query = f"SELECT device_id, name, status, temperature, location FROM devices WHERE temperature BETWEEN {adjusted_min_temp} AND {adjusted_max_temp} AND status = '{device_status}'"

# Execute the query and print the results
cursor.execute(query)
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()