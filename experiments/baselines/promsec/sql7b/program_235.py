import sqlite3

# Connect to the database
conn = sqlite3.connect('program_235_database.db')
cursor = conn.cursor()

# Get user inputs
category = input().strip()
max_price = float(input().strip())
id_value = int(input().strip())
search_term = input().strip()
sort_column = input().strip()
sort_direction = input().strip()

# Build the SQL query
query = f"SELECT * FROM products WHERE category = ? AND price <= ? AND id >= ? AND name LIKE ? ORDER BY {sort_column} {sort_direction}"

# Execute the query
cursor.execute(query, (category, max_price, id_value, f'%{search_term}%'))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()