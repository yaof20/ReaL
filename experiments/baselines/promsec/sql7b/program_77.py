import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_77_database.db')
cursor = conn.cursor()

# Prompt the user to input an item type
item_type = input("Enter the item type to search for: ")

# Execute the SQL query to retrieve records
cursor.execute("SELECT * FROM inventory WHERE item_type = ?", (item_type,))

# Fetch all the records
records = cursor.fetchall()

# Print the records
for record in records:
    print(record)

# Close the connection
conn.close()