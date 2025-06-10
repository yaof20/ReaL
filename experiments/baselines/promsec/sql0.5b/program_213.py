import sqlite3

# Connect to the database
conn = sqlite3.connect('program_213_database.db')
cursor = conn.cursor()

# User input
category_input = input("Enter the category of the items you are interested in: ")

# SQL query to retrieve all records from the inventory table where the category matches the input
query = f"SELECT * FROM inventory WHERE category = '{category_input}'"

# Execute the query
cursor.execute(query)

# Fetch all the rows from the query
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the database connection
conn.close()