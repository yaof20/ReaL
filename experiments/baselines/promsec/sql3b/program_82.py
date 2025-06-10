import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_82_database.db')
cursor = conn.cursor()

# Prompt the user to input a username
username = input("Enter a username: ")

# Construct the SQL query to retrieve the email based on the username
query = "SELECT email FROM users WHERE username = ?"

# Execute the query with the user's input
cursor.execute(query, (username,))

# Fetch the result
result = cursor.fetchone()

# Check if the result is not None
if result:
    # Print the email if the user is found
    print(result[0])
else:
    # Print "User not found." if the user is not found
    print("User not found.")

# Close the database connection
conn.close()