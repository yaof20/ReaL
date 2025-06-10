import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_348_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
customer_name = input("Enter customer name: ")
min_price = float(input("Enter minimum price: "))
max_price = float(input("Enter maximum price: "))

# Build the SQL query
query = f"""
SELECT order_id, item, quantity, price, customer
FROM orders
WHERE customer = ? AND price BETWEEN ? AND ?
"""

# Execute the query with user inputs
cursor.execute(query, (customer_name, min_price, max_price))

# Fetch all the results
results = cursor.fetchall()

# Print the results
print(results)

# Close the database connection
conn.close()