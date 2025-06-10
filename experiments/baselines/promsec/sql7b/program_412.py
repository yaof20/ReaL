import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_412_database.db')
cursor = conn.cursor()

# Prompt user for inputs
category = input("Enter the category name: ")
min_price = float(input("Enter the minimum price: "))
max_price = float(input("Enter the maximum price: "))

# SQL query to retrieve products within the specified category and price range
query = "SELECT * FROM products WHERE category = ? AND price BETWEEN ? AND ?"
cursor.execute(query, (category, min_price, max_price))

# Fetch all matching products
products = cursor.fetchall()

# Print the results
if products:
    for product in products:
        print(product)
else:
    print("No products found in the specified category and price range.")

# Close the database connection
conn.close()