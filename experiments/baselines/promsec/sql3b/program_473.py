import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_473_database.db')
cursor = conn.cursor()

# Prompt user for inputs
username = input("Enter a username to search for: ")
email_domain = input("Enter an email domain to search within (e.g., .com, .org): ")
order_column = input("Enter the column to order the results by (username, email, bio): ")
order_type = input("Enter the order type (ASC for ascending, DESC for descending): ")

# Construct the SQL query
query = f"""
SELECT * FROM users
WHERE username = ? OR email LIKE ? || '%'
ORDER BY {order_column} {order_type}
"""

# Execute the query with user inputs
cursor.execute(query, (username, email_domain))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()