import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_34_database.db')
cursor = conn.cursor()

# Prompt the user for a search term
search_term = input("Enter the product name to search for: ")

# Construct the SQL query
query = f"SELECT * FROM products WHERE name = '{search_term}'"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()