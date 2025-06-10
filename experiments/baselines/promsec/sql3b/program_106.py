import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_106_database.db')
cursor = conn.cursor()

# Prompt the user to input a last name
last_name = input("Enter a last name: ")

# Sanitize the input to remove non-alphabetic characters
last_name = ''.join(filter(str.isalpha, last_name))

# Construct the SQL query
query = f"SELECT employee_id, first_name, last_name, department, salary FROM employees WHERE last_name = '{last_name}'"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()