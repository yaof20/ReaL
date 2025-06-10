import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_8_database.db')
cursor = conn.cursor()

# Prompt the user to input an item name
item_name = input("Enter the item name to search for: ")

# Construct the SQL query to search for the item by name
query = f"SELECT * FROM inventory WHERE item_name = ?"

# Execute the query with the user's input
cursor.execute(query, (item_name,))

# Fetch all the results
results = cursor.fetchall()

# Print the results
if results:
    for row in results:
        print(row)
else:
    print("No items found with the given name.")

# Close the database connection
conn.close()