import sqlite3

# Connect to the database
conn = sqlite3.connect('program_295_database.db')
cursor = conn.cursor()

# Get user inputs
account_id = int(input())
min_balance = float(input())

# Build the SQL query
query = f"SELECT account_id, account_holder, balance FROM accounts WHERE account_id = {account_id} AND balance >= {min_balance}"

# Execute the query
cursor.execute(query)

# Fetch all results
results = cursor.fetchall()

# Print the results
print(results)

# Close the connection
conn.close()