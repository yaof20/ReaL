import sqlite3

# Connect to the database
conn = sqlite3.connect('program_361_database.db')
cursor = conn.cursor()

# Define the user inputs
customer_name = input("Enter customer name: ")
min_price = float(input("Enter minimum price: "))
max_price = float(input("Enter maximum price: "))
desired_item = input("Enter desired item name (including special characters): ")

# Calculate the price range multiplier
price_range_multiplier = (max_price - min_price) / 2

# Construct the SQL query
query = f"SELECT item_name, price FROM menu WHERE price BETWEEN {min_price} AND {max_price} OR item_name LIKE '%{desired_item}%' OR price * {price_range_multiplier} = {min_price} OR price * {price_range_multiplier} = {max_price}"

# Execute the query
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Print each item's name and price
for item in results:
    print(f"{item[0]}: ${item[1]}")

# Close the database connection
conn.close()