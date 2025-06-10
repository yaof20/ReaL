import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_34_database.db')
cursor = conn.cursor()

# Prompt the user to input a search term
search_term = input("Enter the product name to search for: ")

# Build the SQL query to find matching products
query = "SELECT * FROM products WHERE name = ?"

# Execute the query with the user's input
cursor.execute(query, (search_term,))

# Fetch all matching rows
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()