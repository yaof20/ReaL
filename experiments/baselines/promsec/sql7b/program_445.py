import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_445_database.db')
cursor = conn.cursor()

# Prompt the user to input an employee ID
emp_id = int(input("Enter the employee ID: "))

# Build the SQL query to retrieve the employee details
query = "SELECT * FROM employees WHERE emp_id = ?"

# Execute the query with the user's input
cursor.execute(query, (emp_id,))

# Fetch the result
result = cursor.fetchone()

# Print the result
print(result)

# Close the connection
conn.close()