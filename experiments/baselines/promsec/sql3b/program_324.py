import sqlite3

# Connect to the database
conn = sqlite3.connect('program_324_database.db')
cursor = conn.cursor()

# Get the student ID from the user
student_id = int(input())

# Construct the SQL query
query = f"SELECT * FROM students WHERE id = {student_id}"

# Execute the query
cursor.execute(query)

# Fetch the result
result = cursor.fetchone()

# Print the result
if result:
    print(result)
else:
    print([])

# Close the connection
conn.close()