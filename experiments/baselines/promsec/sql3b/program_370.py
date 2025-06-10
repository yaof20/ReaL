import sqlite3

# Connect to the database
conn = sqlite3.connect('program_370_database.db')
cursor = conn.cursor()

# Get user inputs
min_balance = float(input("Enter the minimum account balance: "))
max_balance = float(input("Enter the maximum account balance: "))
bonus_percentage = float(input("Enter the bonus percentage: "))
membership_level = input("Enter the membership level: ")

# Calculate effective balance range
effective_min_balance = min_balance * (1 + bonus_percentage)
effective_max_balance = max_balance * (1 + bonus_percentage)

# Construct the SQL query
query = f"""
SELECT customer_id, first_name, last_name, email, balance, membership_level
FROM customer_info
WHERE (balance BETWEEN {effective_min_balance} AND {effective_max_balance})
OR membership_level = '{membership_level}'
"""

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()