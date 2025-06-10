import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_424_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    search_field = input("Enter the search field (first_name, last_name, email, or phone): ")
    search_value = input("Enter the search value: ")
    sort_field = input("Enter the field to sort by (customer_id, first_name, last_name, email, or phone): ")
    sort_order = input("Enter the order direction (ASC or DESC): ")

    # Construct the SQL query based on the user's inputs
    query = f"SELECT * FROM customers WHERE {search_field} = ? AND {sort_field} = ? ORDER BY {sort_order}"

    # Execute the query
    cursor.execute(query, (search_value, sort_value))

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()