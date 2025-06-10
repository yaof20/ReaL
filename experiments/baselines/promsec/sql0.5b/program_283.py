import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_283_database.db')
cursor = conn.cursor()

# Prompt the user for department name and minimum salary
department_name = input("Enter the department name: ")
min_salary = float(input("Enter the minimum salary: "))

# Construct the SQL query
query = f"SELECT emp_id, emp_name, department, salary FROM employees WHERE department = '{department_name}' AND salary >= {min_salary}"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()