import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_283_database.db')
cursor = conn.cursor()

# Prompt user for inputs
department = input("Enter the department name: ")
min_salary = float(input("Enter the minimum salary: "))

# Construct the SQL query
query = "SELECT * FROM employees WHERE department = ? AND salary >= ?"

# Execute the query
cursor.execute(query, (department, min_salary))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()