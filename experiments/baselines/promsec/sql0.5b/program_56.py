import sqlite3

def connect_to_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_56_database.db')
    return conn

def query_items_by_name(conn, user_input):
    # Create a cursor object
    cursor = conn.cursor()
    
    # Sanitize the user input by removing special characters
    sanitized_input = user_input.replace(" ", "").replace("'", "")
    
    # Construct the SQL query
    query = f"SELECT item_id, item_name, category, stock_quantity, price_per_unit FROM items WHERE item_name LIKE ?"
    
    # Execute the query
    cursor.execute(query, (sanitized_input,))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for item in results:
        print(item)

def main():
    # Connect to the database
    conn = connect_to_database()
    
    # Prompt the user for input
    user_input = input("Enter the item name to search for: ")
    
    # Query the items by name
    query_items_by_name(conn, user_input)
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()