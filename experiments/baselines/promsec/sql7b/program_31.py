import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_31_database.db')
cursor = conn.cursor()

# Prompt the user to input an item name
item_name = input("Enter the item name to search for: ")

# SQL query to search for the item in the 'inventory' table
query = "SELECT * FROM inventory WHERE item_name = ?"

# Execute the query with the user's input
cursor.execute(query, (item_name,))

# Fetch all matching records
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()