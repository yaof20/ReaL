import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_469_database.db')
cursor = conn.cursor()

# Get user input
item_name = input("Enter the item name to search for: ")

# Build the SQL query
query = "SELECT * FROM orders WHERE item_name = ?"

# Execute the query
cursor.execute(query, (item_name,))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()