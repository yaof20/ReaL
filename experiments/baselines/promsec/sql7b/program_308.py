import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_308_database.db')
cursor = conn.cursor()

# Prompt user for department and maximum cost
department = input("Enter the department name: ")
max_cost = float(input("Enter the maximum cost: "))

# SQL query to retrieve products based on department and cost
query = "SELECT * FROM products WHERE department = ? AND cost <= ?"
cursor.execute(query, (department, max_cost))

# Fetch all matching products
products = cursor.fetchall()

# Print the results
for product in products:
    print(product)

# Close the database connection
conn.close()