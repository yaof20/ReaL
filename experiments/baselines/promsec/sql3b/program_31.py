import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_31_database.db')
cursor = conn.cursor()

# Prompt the user to input an item name
item_name = input("Enter the item name to search for: ")

# Construct the SQL query to search for the item
query = f"SELECT * FROM inventory WHERE item_name = '{item_name}'"

# Execute the query
cursor.execute(query)

# Fetch all matching records
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()