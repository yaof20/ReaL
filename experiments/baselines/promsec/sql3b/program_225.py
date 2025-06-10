import sqlite3

def search_users():
    # Connect to the database
    conn = sqlite3.connect('program_225_database.db')
    cursor = conn.cursor()
    
    # Get user input
    search_term = input("Enter the search term: ")
    filter_type = input("Enter the filter type (username or email): ")
    
    # Build the SQL query based on the filter type
    if filter_type == 'username':
        query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%'"
    elif filter_type == 'email':
        query = f"SELECT * FROM users WHERE email LIKE '%{search_term}%'"
    else:
        print("Invalid filter type. Please enter 'username' or 'email'.")
        return
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    if results:
        for row in results:
            print(row)
    else:
        print("No results found.")
    
    # Close the connection
    conn.close()

# Call the function
search_users()