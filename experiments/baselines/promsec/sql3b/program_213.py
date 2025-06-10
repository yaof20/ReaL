import sqlite3

# Connect to the database
conn = sqlite3.connect('program_213_database.db')
cursor = conn.cursor()

# Get user input for the category
category = input("Enter the category: ")

# Construct the SQL query
query = f"SELECT * FROM inventory WHERE category = '{category}'"

# Execute the query
cursor.execute(query)

# Fetch all the rows that match the category
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the connection
conn.close()