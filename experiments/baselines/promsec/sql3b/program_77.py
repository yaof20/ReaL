import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_77_database.db')
cursor = conn.cursor()

# Prompt the user to input an item type
item_type = input("Enter the item type to search for: ")

# Construct the SQL query
query = f"SELECT * FROM inventory WHERE item_type = '{item_type}'"

# Execute the query
cursor.execute(query)

# Fetch all the records
records = cursor.fetchall()

# Print the results
for record in records:
    print(record)

# Close the database connection
conn.close()