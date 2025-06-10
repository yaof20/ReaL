import sqlite3

def fetch_menu_items():
    # Connect to the database
    conn = sqlite3.connect('program_361_database.db')
    cursor = conn.cursor()
    
    # Get user inputs
    customer_name = input("Enter customer name: ")
    min_price = float(input("Enter minimum price: "))
    max_price = float(input("Enter maximum price: "))
    desired_item = input("Enter desired item name: ")
    
    # Calculate price range multiplier
    price_range_multiplier = max_price - min_price
    
    # Construct SQL query
    query = """
    SELECT item_name, price
    FROM menu
    WHERE (price BETWEEN ? AND ?)
    OR (item_name LIKE ?)
    OR (price = ?)
    """
    cursor.execute(query, (min_price, max_price, f"%{desired_item}%", price_range_multiplier))
    
    # Fetch results
    results = cursor.fetchall()
    
    # Print results
    for item in results:
        print(f"{item[0]} {item[1]}")
    
    # Close the database connection
    conn.close()

# Call the function
fetch_menu_items()