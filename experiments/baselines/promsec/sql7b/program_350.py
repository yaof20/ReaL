import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_350_database.db')
cursor = conn.cursor()

# Prompt user for inputs
customer_name = input("Enter customer name: ")
min_balance = float(input("Enter minimum balance: "))

# Build the SQL query
query = "SELECT * FROM customers WHERE name = ? AND balance > ?"

# Execute the query
cursor.execute(query, (customer_name, min_balance))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()