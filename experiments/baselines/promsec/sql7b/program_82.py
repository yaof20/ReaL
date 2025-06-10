import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_82_database.db')
cursor = conn.cursor()

# Prompt the user to input a username
username = input("Enter a username: ")

# SQL query to retrieve the email based on the username
query = "SELECT email FROM users WHERE username = ?"

# Execute the query
cursor.execute(query, (username,))

# Fetch the result
result = cursor.fetchone()

# Check if the user was found and print the result
if result:
    print(result[0])
else:
    print("User not found.")

# Close the database connection
conn.close()