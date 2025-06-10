import sqlite3

def search_inventory():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_89_database.db')
    cursor = conn.cursor()

    # Prompt the user to input a field to search by
    field = input("Enter the field to search by (item_id, item_name, category): ")

    # Prompt the user to input a value to search for
    value = input("Enter the value to search for: ")

    # Construct the SQL query based on the user's input
    query = f"SELECT * FROM inventory WHERE {field} = ?"

    try:
        # Execute the query with the provided value
        cursor.execute(query, (value,))
        
        # Fetch all rows from the query result
        rows = cursor.fetchall()
        
        # Print the results
        for row in rows:
            print(row)
    
    except sqlite3.Error as e:
        # Handle any potential errors during query execution
        print(f"An error occurred: {e}")
    
    finally:
        # Close the database connection
        conn.close()

# Call the function to start the search
search_inventory()