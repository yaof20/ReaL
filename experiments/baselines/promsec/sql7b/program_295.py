import sqlite3

# Connect to the database
conn = sqlite3.connect('program_295_database.db')
cursor = conn.cursor()

# Get user inputs
account_id = int(input())
min_balance = float(input())

# Build and execute the SQL query
query = "SELECT * FROM accounts WHERE account_id = ? AND balance >= ?"
cursor.execute(query, (account_id, min_balance))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()