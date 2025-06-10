import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_269_database.db')
cursor = conn.cursor()

# Get user inputs
min_stock = int(input("Enter the minimum stock threshold: "))
max_price = float(input("Enter the maximum price: "))
category = input("Enter the product category: ")

# Build the SQL query
query = f"""
SELECT product_id, product_name, category, stock, price
FROM inventory
WHERE stock > {min_stock}
  AND price < {max_price}
  AND category = '{category}'
"""

# Execute the query
cursor.execute(query)

# Fetch all results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()