import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_473_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    username = input("Enter a username to search for: ")
    email_domain = input("Enter an email domain to search within (like .com or .org): ")
    column_to_order = input("Enter the column to order the results by (either 'username', 'email', or 'bio'): ")
    order_type = input("Enter the order type (either 'ASC' for ascending or 'DESC' for descending): ")

    # Construct the SQL query
    query = f"SELECT * FROM users WHERE {column_to_order} LIKE ? OR {column_to_order} LIKE ? AND {column_to_order} LIKE ?"

    # Execute the query
    cursor.execute(query, (username, email_domain, column_to_order, order_type))

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()