import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_231_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
account_number = input("Enter the account number: ")
min_amount = float(input("Enter the minimum transaction amount: "))

# Build the SQL query
query = f"""
SELECT transaction_id, account_number, amount, transaction_date, description
FROM transactions
WHERE account_number = ? AND amount >= ?
"""

# Execute the query with user inputs
cursor.execute(query, (account_number, min_amount))

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()