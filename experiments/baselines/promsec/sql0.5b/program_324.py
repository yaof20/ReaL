import sqlite3

def fetch_student_by_id(student_id):
    # Connect to the database
    conn = sqlite3.connect('program_324_database.db')
    cursor = conn.cursor()
    
    # Define the SQL query to fetch the student by ID
    query = f"SELECT * FROM students WHERE id = {student_id}"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the rows from the query
    rows = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Print the results
    if rows:
        print(rows)
    else:
        print("No student found with the given ID.")

# Example usage
input_id = input("Enter the student ID: ")
fetch_student_by_id(input_id)