import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_191_database.db')
cursor = conn.cursor()

# Get user inputs
customer_name = input("Enter customer name: ")
min_quantity = int(input("Enter minimum quantity: "))
dish_type = input("Enter dish type preference: ")
price_limit = float(input("Enter price limit: "))

# Construct the SQL query
query = """
SELECT order_id, customer_name, dish, quantity, price
FROM orders
WHERE customer_name = ? AND (
    quantity >= ? OR
    dish = ? OR
    price <= ?
)
"""

# Execute the query with user inputs
cursor.execute(query, (customer_name, min_quantity, dish_type, price_limit))

# Fetch all results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()