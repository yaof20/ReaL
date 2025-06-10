import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_170_database.db')
cursor = conn.cursor()

# Prompt the user to enter a customer name
customer_name = input("Enter customer name: ")

# Execute the query to fetch all orders for the specified customer
cursor.execute("SELECT * FROM sales WHERE customer_name = ?", (customer_name,))

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()