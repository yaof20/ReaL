import sqlite3

# Connect to the database
conn = sqlite3.connect('program_213_database.db')
cursor = conn.cursor()

# Get user input
category = input("Enter the category of items you are interested in: ")

# Build SQL query
query = "SELECT * FROM inventory WHERE category = ?"

# Execute the query
cursor.execute(query, (category,))

# Fetch all matching records
records = cursor.fetchall()

# Print the results
for record in records:
    print(record)

# Close the connection
conn.close()