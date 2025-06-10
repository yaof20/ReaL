import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_269_database.db')
cursor = conn.cursor()

# Get user inputs
min_stock = int(input("Enter minimum stock threshold: "))
max_price = float(input("Enter maximum price: "))
category = input("Enter product category: ")

# Build the SQL query
query = """
SELECT product_id, product_name, category, stock, price
FROM inventory
WHERE stock > ? AND price < ? AND category = ?
"""

# Execute the query with user inputs
cursor.execute(query, (min_stock, max_price, category))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()