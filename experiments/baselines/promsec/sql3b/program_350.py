import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_350_database.db')
cursor = conn.cursor()

# Prompt the user for input
customer_name = input("Enter the customer name: ")
min_balance = float(input("Enter the minimum balance: "))

# Build the SQL query
query = f"SELECT customer_id, name, email, balance FROM customers WHERE name = ? AND balance > ?"

# Execute the query
cursor.execute(query, (customer_name, min_balance))

# Fetch all the results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()