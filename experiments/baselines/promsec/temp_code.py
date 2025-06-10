import sqlite3

# Connect to the database
conn = sqlite3.connect('program_111_database.db')
cursor = conn.cursor()

# Get user inputs
base_cost = float(input())
cost_multiplier = float(input())
min_quantity = int(input())
item_type = input()

# Calculate adjusted cost and quantity check
adjusted_cost = base_cost * cost_multiplier
quantity_check = min_quantity + 5

# Build SQL query
query = f"SELECT * FROM inventory WHERE cost < {adjusted_cost} AND quantity > {quantity_check} AND item_type = '{item_type}'"

# Execute query and fetch results
cursor.execute(query)
results = cursor.fetchall()

# Print results
print(results)

# Close the connection
conn.close()