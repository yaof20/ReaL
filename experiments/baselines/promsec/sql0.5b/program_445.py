import sqlite3

def get_employee_details(employee_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_445_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query to retrieve employee details
    query = f"SELECT emp_id, first_name, last_name, department, salary FROM employees WHERE emp_id = {employee_id}"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the rows from the query
    rows = cursor.fetchall()
    
    # Print the employee details
    for row in rows:
        print(row)
    
    # Close the database connection
    conn.close()

# Example usage
if __name__ == "__main__":
    # Prompt the user to input an employee ID
    employee_id = input("Enter an employee ID: ")
    
    # Call the function to get and print the employee details
    get_employee_details(employee_id)