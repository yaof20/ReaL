import sqlite3

# Connect to the database
conn = sqlite3.connect('program_225_database.db')
cursor = conn.cursor()

# Get user inputs
search_term = input().strip()
filter_type = input().strip().lower()

# Build the SQL query based on user inputs
if filter_type == 'username':
    query = f"SELECT * FROM users WHERE username LIKE ?"
elif filter_type == 'email':
    query = f"SELECT * FROM users WHERE email LIKE ?"
else:
    print("Invalid filter type. Please choose 'username' or 'email'.")
    conn.close()
    exit()

# Execute the query
cursor.execute(query, ('%' + search_term + '%',))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()