import sqlite3

def get_student_gpa(student_name, view_gpa):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_275_database.db')
    cursor = conn.cursor()
    
    # Check if the student exists in the database
    cursor.execute("SELECT * FROM students WHERE name = ?", (student_name,))
    student = cursor.fetchone()
    
    if student:
        # Check if the GPA is greater than 0
        if view_gpa == 'yes':
            cursor.execute("SELECT * FROM students WHERE name = ? AND gpa > 0", (student_name,))
        else:
            cursor.execute("SELECT * FROM students WHERE name = ?", (student_name,))
    
        # Fetch all columns from the result
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        
        # Print the results
        print(f"Student: {student[1]}, GPA: {results[0][3]}")
    else:
        print("Student not found.")
    
    # Close the database connection
    conn.close()

# Example usage
get_student_gpa('Charlie', 'yes')
get_student_gpa('David', 'no')