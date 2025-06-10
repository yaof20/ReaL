import sqlite3

def search_users(db_path, search_term, filter_type):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Define the SQL query based on the filter type
    if filter_type == 'username':
        query = f"SELECT * FROM users WHERE username LIKE ?"
    elif filter_type == 'email':
        query = f"SELECT * FROM users WHERE email LIKE ?"
    else:
        return "Invalid filter type. Please choose 'username' or 'email'."
    
    # Execute the query with the search term
    cursor.execute(query, (search_term,))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the database connection
    conn.close()

# Example usage
db_path = 'program_225_database.db'
search_term = input("Enter a search term: ")
filter_type = input("Enter 'username' or 'email': ")
search_users(db_path, search_term, filter_type)