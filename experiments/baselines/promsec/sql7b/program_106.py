import sqlite3
import re

# Connect to the SQLite database
conn = sqlite3.connect('program_106_database.db')
cursor = conn.cursor()

# Function to sanitize input
def sanitize_input(input_string):
    return re.sub(r'[^a-zA-Z\s]', '', input_string)

# Prompt user for last name
last_name = input("Enter the last name to search for: ").strip()
sanitized_last_name = sanitize_input(last_name)

# SQL query to fetch employees with the given last name
query = "SELECT * FROM employees WHERE last_name = ?"

# Execute the query
cursor.execute(query, (sanitized_last_name,))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()