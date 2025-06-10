import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_463_database.db')
cursor = conn.cursor()

# Prompt the user to enter the item name to search for
item_name = input("Enter the name of the item to search for: ")

# Construct the SQL query to find the item(s) with the specified name
query = f"SELECT * FROM inventory WHERE item_name = '{item_name}'"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()