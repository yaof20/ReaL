# Import necessary libraries
import sqlite3

# Connect to the database
conn = sqlite3.connect('program_111_database.db')
cursor = conn.cursor()

# Define the user inputs
base_cost = float(input("Enter the base cost: "))
cost_multiplier = float(input("Enter the cost multiplier: "))
min_quantity_threshold = int(input("Enter the minimum quantity threshold: "))
item_type = input("Enter the item type: ")

# Calculate the adjusted cost
adjusted_cost = base_cost * cost_multiplier

# Calculate the quantity check
quantity_check = min_quantity_threshold + 5

# Construct the SQL query
query = f"SELECT * FROM inventory WHERE cost < {adjusted_cost} AND quantity > {quantity_check} AND item_type = '{item_type}'"

# Execute the query
cursor.execute(query)

# Fetch all the items that match the conditions
items = cursor.fetchall()

# Print the retrieved items
for item in items:
    print(item)

# Close the database connection
conn.close()