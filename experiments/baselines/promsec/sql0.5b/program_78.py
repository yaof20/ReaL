import sqlite3

def get_orders(start_date, end_date, bulk_discount_percentage, order_status, price_threshold):
    # Connect to the database
    conn = sqlite3.connect('program_78_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = """
    SELECT order_id, customer, order_date, status, total_price
    FROM orders
    WHERE order_date BETWEEN ? AND ?
    AND status = ?
    AND total_price > ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (start_date, end_date, order_status, price_threshold))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for order in results:
        print(order)
    
    # Close the database connection
    conn.close()

# Example usage
get_orders('2023-01-01', '2023-12-31', 10, 'Pending', 600)
get_orders('2023-01-01', '2023-12-31', 25, 'Pending', 500)