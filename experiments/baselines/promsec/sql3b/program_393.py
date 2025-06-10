import sqlite3

def get_student_record(student_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_393_database.db')
    cursor = conn.cursor()
    
    # Prepare the SQL query
    query = "SELECT * FROM students WHERE student_id = ?"
    
    try:
        # Execute the query with the provided student ID
        cursor.execute(query, (student_id,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        if result:
            # Print the result
            print(result)
        else:
            # Print an error message if no record is found
            print("An error occurred: no record found for the given student ID")
    
    except sqlite3.Error as e:
        # Print an error message if an error occurs during the query execution
        print(f"An error occurred: {e}")
    
    finally:
        # Close the database connection
        conn.close()

# Prompt the user to input a student ID
student_id = input("Enter a student ID: ")

# Call the function to get the student record
get_student_record(student_id)