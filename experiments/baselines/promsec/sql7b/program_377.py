import sqlite3

# Connect to the database
conn = sqlite3.connect('program_377_database.db')
cursor = conn.cursor()

# Prompt user for inputs
min_amount = float(input("Enter minimum transaction amount: "))
max_amount = float(input("Enter maximum transaction amount: "))
category = input("Enter transaction category: ")

# Construct SQL query
query = "SELECT * FROM transactions WHERE (amount BETWEEN ? AND ?) OR category = ?"
cursor.execute(query, (min_amount, max_amount, category))

# Fetch and print results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()