import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_463_database.db')
cursor = conn.cursor()

# Get user input for the item name to search
item_name = input("Enter the item name to search for: ")

# SQL query to find items with the specified name
query = "SELECT * FROM inventory WHERE item_name = ?"

# Execute the query
cursor.execute(query, (item_name,))

# Fetch all matching items
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()