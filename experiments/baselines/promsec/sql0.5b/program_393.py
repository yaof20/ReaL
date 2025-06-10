import sqlite3

def get_student_info(student_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_393_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query to retrieve the student's information
    query = f"SELECT * FROM students WHERE student_id = {student_id}"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the database connection
    conn.close()
    
    # Print the result
    if result:
        print(result)
    else:
        print("An error occurred: incomplete input")

# Example usage
get_student_info(104)