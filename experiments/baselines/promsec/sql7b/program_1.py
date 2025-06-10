import sqlite3

# Connect to the database
conn = sqlite3.connect('program_1_database.db')
cursor = conn.cursor()

# Get user input
customer_name = input("Enter customer name: ")

# Build SQL query
query = "SELECT * FROM orders WHERE customer_name = ?"

# Execute the query
cursor.execute(query, (customer_name,))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()