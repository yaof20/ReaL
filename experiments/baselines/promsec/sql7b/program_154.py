import sqlite3

# Connect to the database
conn = sqlite3.connect('program_154_database.db')
cursor = conn.cursor()

# Get user input
location = input("Enter the location: ")

# Build the SQL query
query = "SELECT * FROM listings WHERE location = ?"

# Execute the query
cursor.execute(query, (location,))

# Fetch all matching records
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()