import sqlite3

# Connect to the database
conn = sqlite3.connect('program_430_database.db')
cursor = conn.cursor()

# Prompt user for input
payer_name = input("Enter the payer's name: ")
min_amount = float(input("Enter the minimum amount: "))

# Build the SQL query
query = "SELECT * FROM transactions WHERE payer = ? AND amount >= ?"

# Execute the query
cursor.execute(query, (payer_name, min_amount))

# Fetch and print all matching records
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()