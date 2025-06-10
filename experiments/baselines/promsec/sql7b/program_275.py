import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_275_database.db')
cursor = conn.cursor()

# Get user inputs
student_name = input("Enter the student's name: ")
view_gpa_details = input("Do you want to view GPA details? (yes/no): ")

# Construct the SQL query based on user inputs
if view_gpa_details.lower() == 'yes':
    query = "SELECT * FROM students WHERE name = ? AND gpa > 0"
else:
    query = "SELECT * FROM students WHERE name = ?"

# Execute the query
cursor.execute(query, (student_name,))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()