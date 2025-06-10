import sqlite3

# Connect to the database
conn = sqlite3.connect('program_361_database.db')
cursor = conn.cursor()

# Get user inputs
customer_name = input().strip()
min_price = float(input().strip())
max_price = float(input().strip())
desired_item = input().strip()

# Calculate the price range multiplier
price_range_multiplier = max_price / min_price

# Construct the SQL query
query = f"""
SELECT item_name, price
FROM menu
WHERE price BETWEEN {min_price} AND {max_price}
OR item_name LIKE '%{desired_item}%'
OR price = {price_range_multiplier}
"""

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for item in results:
    print(f"{item[0]} {item[1]}")

# Close the database connection
conn.close()