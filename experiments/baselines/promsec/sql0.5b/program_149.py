import sqlite3

# Connect to the database
conn = sqlite3.connect('program_149_database.db')
cursor = conn.cursor()

# Prompt the user for input
item_id = input("Enter the item id: ")
description = input("Enter the description: ")

# Construct the SQL query
query = f"SELECT * FROM items WHERE id = {item_id} OR description LIKE '%{description}%'"

# Execute the query
cursor.execute(query)

# Fetch all the records
records = cursor.fetchall()

# Print the results
for record in records:
    print(record)

# Close the database connection
conn.close()