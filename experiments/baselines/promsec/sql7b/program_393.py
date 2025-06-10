import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_393_database.db')
cursor = conn.cursor()

# Prompt the user to input a student ID
student_id = input("Enter a student ID: ")

# Check if the input is empty
if not student_id:
    print("An error occurred: incomplete input")
else:
    # Build the SQL query to retrieve the student record
    query = "SELECT * FROM students WHERE student_id = ?"
    
    # Execute the query
    cursor.execute(query, (student_id,))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Check if a record was found
    if result:
        print(result)
    else:
        print("No student found with the given ID.")

# Close the database connection
conn.close()