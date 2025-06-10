import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_473_database.db')
cursor = conn.cursor()

# Prompt user for inputs
username_search = input("Enter username to search for: ")
email_domain = input("Enter email domain to search within (e.g., .com): ")
order_column = input("Enter column to order the results by (username, email, bio): ")
order_type = input("Enter order type (ASC for ascending, DESC for descending): ")

# Construct the SQL query
query = f"SELECT * FROM users WHERE username = ? OR email LIKE ? ORDER BY {order_column} {order_type}"
email_pattern = f'%@{email_domain}'

# Execute the query
cursor.execute(query, (username_search, email_pattern))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()