import sqlite3

# Connect to the database
conn = sqlite3.connect('program_430_database.db')
cursor = conn.cursor()

# Prompt the user for input
payer_name = input("Enter the payer's name: ")
min_amount = float(input("Enter the minimum amount: "))

# Build the SQL query
query = f"SELECT * FROM transactions WHERE payer = ? AND amount >= ?"

# Execute the query
cursor.execute(query, (payer_name, min_amount))

# Fetch all matching records
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()