import sqlite3

def get_orders_by_price_and_category(min_price, max_price, category):
    # Connect to the database
    conn = sqlite3.connect('program_248_database.db')
    cursor = conn.cursor()
    
    # Define the SQL query
    query = """
    SELECT order_id, item, category, price, quantity
    FROM orders
    WHERE price BETWEEN ? AND ?
    AND category = ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (min_price, max_price, category))
    
    # Fetch all the results
    orders = cursor.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Return the list of orders
    return orders

# Example usage
min_price = float(input("Enter the minimum price: "))
max_price = float(input("Enter the maximum price: "))
category = input("Enter the category: ")

orders = get_orders_by_price_and_category(min_price, max_price, category)
print(orders)