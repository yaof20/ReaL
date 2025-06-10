import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_106_database.db')
    cursor = conn.cursor()

    # Prompt the user for input
    last_name = input("Enter the last name: ")

    # Sanitize the input to remove non-alphabetic characters
    sanitized_last_name = ''.join(char.lower() for char in last_name if char.isalpha())

    # Construct the SQL query
    query = f"SELECT employee_id, first_name, last_name, department, salary FROM employees WHERE last_name = '{sanitized_last_name}'"

    # Execute the query
    cursor.execute(query)

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()