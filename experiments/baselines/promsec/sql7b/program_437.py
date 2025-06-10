import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_437_database.db')
cursor = conn.cursor()

# Prompt the user to input an account number
account_number = int(input("Enter an account number: "))

# SQL query to fetch the holder's name and balance
query = "SELECT holder_name, balance FROM accounts WHERE account_number = ?"

# Execute the query
cursor.execute(query, (account_number,))

# Fetch the result
result = cursor.fetchone()

# Check if the account is found
if result:
    print(f"Holder's Name: {result[0]}, Balance: {result[1]}")
else:
    print("Account not found.")

# Close the connection
conn.close()