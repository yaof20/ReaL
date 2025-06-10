import sqlite3

# Connect to the database
conn = sqlite3.connect('program_149_database.db')
cursor = conn.cursor()

# Get user inputs
item_id = input("Enter item id: ")
description = input("Enter description: ")

# Construct the SQL query
query = "SELECT * FROM items WHERE id = ? OR description LIKE ?"
cursor.execute(query, (item_id, '%' + description + '%'))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()