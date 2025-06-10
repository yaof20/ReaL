import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_69_database.db')
cursor = conn.cursor()

# Get user inputs
customer_name = input("Enter customer name (exact or partial): ")
product = input("Enter product name: ")
min_amount = float(input("Enter minimum amount: "))

# Construct the SQL query
query = """
SELECT * FROM orders
WHERE customer_name LIKE ? AND product = ? AND amount >= ?
"""
# Execute the query with the user inputs
cursor.execute(query, (f'%{customer_name}%', product, min_amount * 0.9))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()