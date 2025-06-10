import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_202_database.db')
cursor = conn.cursor()

# Prompt user for inputs
phone_number = input("Enter phone number: ")
min_amount_due = float(input("Enter minimum amount due: "))

# Construct SQL query
query = "SELECT * FROM customer_bills WHERE phone = ? AND amount_due > ?"

# Execute the query
cursor.execute(query, (phone_number, min_amount_due))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()