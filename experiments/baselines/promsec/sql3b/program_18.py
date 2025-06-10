import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_18_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
salary_multiplier = float(input("Enter a salary multiplier: "))
bonus_amount = float(input("Enter a bonus amount: "))
department_name = input("Enter a department name: ")

# Calculate the new minimum and maximum salary range
min_salary = salary_multiplier * 5000 + bonus_amount
max_salary = salary_multiplier * 5000 + bonus_amount + 10000

# Construct the SQL query
query = f"""
SELECT id, name, department, salary
FROM employees
WHERE salary BETWEEN {min_salary} AND {max_salary}
AND department = '{department_name}'
"""

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()