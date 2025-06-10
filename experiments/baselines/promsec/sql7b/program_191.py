import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_191_database.db')
cursor = conn.cursor()

# Get user inputs
customer_name = input("Enter customer name for verification: ")
min_quantity = int(input("Enter minimum quantity to filter orders: "))
dish_preference = input("Enter dish type preference: ")
price_limit = float(input("Enter price limit to filter orders: "))

# Construct the SQL query
query = """
SELECT * FROM orders
WHERE customer_name = ? AND (quantity >= ? OR dish = ? OR price <= ?)
"""

# Execute the query
cursor.execute(query, (customer_name, min_quantity, dish_preference, price_limit))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()