import sqlite3

def search_products():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_34_database.db')
    cursor = conn.cursor()
    
    # Prompt the user for input
    search_term = input("Enter a product name to search for: ")
    
    # Construct the SQL query
    query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all rows from the query
    rows = cursor.fetchall()
    
    # Print the results
    for row in rows:
        print(row)
    
    # Close the database connection
    conn.close()

# Call the function to execute the search
search_products()