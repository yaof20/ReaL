import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_275_database.db')
cursor = conn.cursor()

# Function to execute the SQL query
def execute_query(name, view_gpa):
    if view_gpa.lower() == 'yes':
        query = f"SELECT * FROM students WHERE name = ? AND gpa > 0"
    else:
        query = f"SELECT * FROM students WHERE name = ?"
    
    cursor.execute(query, (name,))
    results = cursor.fetchall()
    for row in results:
        print(row)

# Main program
name = input("Enter the name of the student: ")
view_gpa = input("Do you want to view GPA details? (yes/no): ")

# Execute the query
execute_query(name, view_gpa)

# Close the database connection
conn.close()