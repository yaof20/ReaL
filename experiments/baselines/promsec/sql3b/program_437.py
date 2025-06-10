import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_437_database.db')
cursor = conn.cursor()

# Prompt the user to input an account number
account_number = input("Enter the account number: ")

# Construct the SQL query to retrieve the holder's name and balance
query = f"SELECT holder_name, balance FROM accounts WHERE account_number = {account_number}"

# Execute the query
cursor.execute(query)

# Fetch the result
result = cursor.fetchone()

# Check if the result is not None
if result:
    holder_name, balance = result
    print(f"Holder's Name: {holder_name}, Balance: {balance}")
else:
    print("Account not found.")

# Close the connection
conn.close()