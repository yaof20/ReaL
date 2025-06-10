import sqlite3

# Connect to the database
conn = sqlite3.connect('program_324_database.db')
cursor = conn.cursor()

# Get user input
student_id = int(input())

# Build SQL query
query = "SELECT * FROM students WHERE id = ?"

# Execute the query
cursor.execute(query, (student_id,))

# Fetch the result
result = cursor.fetchall()

# Print the result
print(result)

# Close the connection
conn.close()