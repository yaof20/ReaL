import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_283_database.db')
cursor = conn.cursor()

# Prompt the user for department name and minimum salary
department = input("Enter department name: ")
min_salary = float(input("Enter minimum salary: "))

# Construct the SQL query
query = f"SELECT emp_id, emp_name, department, salary FROM employees WHERE department = ? AND salary >= ?"

# Execute the query
cursor.execute(query, (department, min_salary))

# Fetch all results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()