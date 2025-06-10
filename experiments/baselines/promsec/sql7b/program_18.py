import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_18_database.db')
cursor = conn.cursor()

# Prompt user for inputs
salary_multiplier = float(input("Enter the salary multiplier: "))
bonus_amount = float(input("Enter the bonus amount: "))
department_name = input("Enter the department name: ")

# Calculate the new minimum and maximum salary range
min_salary = 0
max_salary = salary_multiplier * 100000 + bonus_amount

# Construct the SQL query
query = f"SELECT * FROM employees WHERE salary BETWEEN {min_salary} AND {max_salary} AND department = ?"

# Execute the query
cursor.execute(query, (department_name,))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()