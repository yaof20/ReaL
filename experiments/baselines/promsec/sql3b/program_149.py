import sqlite3

# Connect to the database
conn = sqlite3.connect('program_149_database.db')
cursor = conn.cursor()

# Prompt the user for input
item_id = input("Enter the item id: ")
description = input("Enter the description: ")

# Construct the SQL query
query = f"SELECT * FROM items WHERE id = ? OR description LIKE ?"
cursor.execute(query, (item_id, f"%{description}%"))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()