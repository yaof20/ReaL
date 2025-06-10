import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_445_database.db')
cursor = conn.cursor()

# Prompt the user to input an employee ID
emp_id = int(input("Enter the employee ID: "))

# Construct the SQL query to retrieve the employee details
query = f"SELECT * FROM employees WHERE emp_id = {emp_id}"

# Execute the query
cursor.execute(query)

# Fetch the result
result = cursor.fetchone()

# Print the result
print(result)

# Close the database connection
conn.close()