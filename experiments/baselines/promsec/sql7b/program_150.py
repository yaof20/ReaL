import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_150_database.db')
cursor = conn.cursor()

# Prompt the user to input a customer name
customer_name = input("Enter customer name: ")

# Build the SQL query to retrieve orders for the given customer
query = "SELECT * FROM orders WHERE customer = ?"

# Execute the query with the user's input
cursor.execute(query, (customer_name,))

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()