import sqlite3

# Connect to the database
conn = sqlite3.connect('program_320_database.db')
cursor = conn.cursor()

# Get user inputs
email = input("Enter email address (leave blank if not applicable): ")
min_balance = float(input("Enter minimum balance: "))
max_balance = float(input("Enter maximum balance: "))

# Build the SQL query
query = "SELECT * FROM customers WHERE 1=1"
if email:
    query += f" AND email = '{email}'"
if min_balance > 0:
    query += f" AND balance >= {min_balance}"
if max_balance > 0:
    query += f" AND balance <= {max_balance}"

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()