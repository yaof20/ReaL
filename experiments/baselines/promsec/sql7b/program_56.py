import sqlite3
import re

# Function to sanitize input
def sanitize_input(user_input):
    # Remove special characters except for alphanumeric and spaces
    sanitized_input = re.sub(r'[^a-zA-Z0-9 ]', '', user_input)
    return sanitized_input

# Connect to the SQLite database
conn = sqlite3.connect('program_56_database.db')
cursor = conn.cursor()

# Prompt user for input
user_input = input("Enter item name to search: ")

# Sanitize the user input
sanitized_input = sanitize_input(user_input)

# Prepare the SQL query
query = f"SELECT * FROM items WHERE item_name LIKE '%{sanitized_input}%'"

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()