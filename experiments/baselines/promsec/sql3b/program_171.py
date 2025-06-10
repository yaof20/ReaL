import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_171_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    department = input("Enter the department name: ")
    column_name = input("Enter the column name to order by: ")
    order_direction = input("Enter the order direction (ASC or DESC): ")

    # Construct the SQL query
    query = f"SELECT emp_id, first_name, last_name FROM employees WHERE department = ? ORDER BY {column_name} {order_direction}"

    try:
        # Execute the query
        cursor.execute(query, (department,))
        results = cursor.fetchall()

        # Print the results
        for row in results:
            print(f"{row[0]} {row[1]} {row[2]}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection
        conn.close()

if __name__ == "__main__":
    main()