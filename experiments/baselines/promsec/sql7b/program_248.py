import sqlite3

# Connect to the database
conn = sqlite3.connect('program_248_database.db')
cursor = conn.cursor()

# Get user inputs
min_price = float(input())
max_price = float(input())
category = input()

# Build the SQL query
query = "SELECT * FROM orders WHERE price BETWEEN ? AND ? AND category = ?"

# Execute the query
cursor.execute(query, (min_price, max_price, category))

# Fetch all matching orders
matching_orders = cursor.fetchall()

# Print the results
print(matching_orders)

# Close the connection
conn.close()