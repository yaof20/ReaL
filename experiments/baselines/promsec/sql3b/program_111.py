import sqlite3

# Connect to the database
conn = sqlite3.connect('program_111_database.db')
cursor = conn.cursor()

# Get user inputs
base_cost = float(input())
cost_multiplier = float(input())
min_quantity_threshold = int(input())
item_type = input()

# Calculate adjusted cost and quantity check
adjusted_cost = base_cost * cost_multiplier
quantity_check = min_quantity_threshold + 5

# Build the SQL query
query = f"""
SELECT item_id, item_name, item_type, quantity, cost
FROM inventory
WHERE cost < {adjusted_cost}
  AND quantity > {quantity_check}
  AND item_type = '{item_type}'
"""

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for item in results:
    print(item)

# Close the connection
conn.close()