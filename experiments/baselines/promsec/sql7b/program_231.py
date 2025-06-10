import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_231_database.db')
cursor = conn.cursor()

# Prompt user for inputs
account_number = input("Enter account number: ")
min_amount = float(input("Enter minimum transaction amount: "))

# Build SQL query based on user inputs
query = "SELECT * FROM transactions WHERE account_number = ? AND amount >= ?"

# Execute the query
cursor.execute(query, (account_number, min_amount))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()