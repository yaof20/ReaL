import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_348_database.db')
cursor = conn.cursor()

# Prompt user for inputs
customer_name = input("Enter customer name: ")
min_price = float(input("Enter minimum price: "))
max_price = float(input("Enter maximum price: "))

# Build SQL query based on user inputs
query = "SELECT * FROM orders WHERE customer = ? AND price BETWEEN ? AND ?"
cursor.execute(query, (customer_name, min_price, max_price))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the database connection
conn.close()