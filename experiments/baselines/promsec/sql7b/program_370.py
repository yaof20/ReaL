import sqlite3

# Connect to the database
conn = sqlite3.connect('program_370_database.db')
cursor = conn.cursor()

# Get user inputs
min_balance = float(input("Enter minimum account balance: "))
max_balance = float(input("Enter maximum account balance: "))
bonus_percentage = float(input("Enter bonus percentage: "))
membership_level = input("Enter membership level: ")

# Calculate effective balance range
effective_min_balance = min_balance * (1 + bonus_percentage)
effective_max_balance = max_balance * (1 + bonus_percentage)

# Construct SQL query
query = """
SELECT * FROM customer_info
WHERE (balance BETWEEN ? AND ?) OR membership_level = ?
"""

# Execute query
cursor.execute(query, (effective_min_balance, effective_max_balance, membership_level))

# Fetch and print results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()