import sqlite3

def sanitize_input(input_str):
    # Remove special characters from the input string
    return ''.join(char for char in input_str if char.isalnum())

def search_items_by_name():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_56_database.db')
    cursor = conn.cursor()
    
    # Prompt the user for input
    user_input = input("Enter the item name to search for: ")
    
    # Sanitize the user input
    sanitized_input = sanitize_input(user_input)
    
    # Construct the SQL query
    query = f"SELECT item_id, item_name, category, stock_quantity, price_per_unit FROM items WHERE item_name LIKE ?"
    
    # Execute the query
    cursor.execute(query, (f"%{sanitized_input}%",))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    if results:
        for row in results:
            print(row)
    else:
        print("No items found.")
    
    # Close the database connection
    conn.close()

# Call the function to execute the search
search_items_by_name()