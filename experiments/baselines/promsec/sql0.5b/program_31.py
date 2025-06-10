import sqlite3

def search_inventory(item_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_31_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query to search for the item
    query = f"SELECT * FROM inventory WHERE item_name = ?"
    
    # Execute the query with the user's input
    cursor.execute(query, (item_name,))
    
    # Fetch all the matching records
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the database connection
    conn.close()

# Example usage
search_inventory(input("Enter an item name: "))