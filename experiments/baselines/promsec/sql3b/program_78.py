import sqlite3

def get_orders():
    # Connect to the database
    conn = sqlite3.connect('program_78_database.db')
    cursor = conn.cursor()
    
    # Prompt user for inputs
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    bulk_discount = float(input("Enter bulk discount percentage: "))
    order_status = input("Enter order status: ")
    price_threshold = float(input("Enter price threshold: "))
    
    # Calculate effective price threshold after applying the discount
    effective_price_threshold = price_threshold * (1 - bulk_discount / 100)
    
    # Construct and execute SQL query
    query = f"""
    SELECT order_id, customer, order_date, status, total_price
    FROM orders
    WHERE order_date BETWEEN '{start_date}' AND '{end_date}'
    AND status = '{order_status}'
    AND total_price > {effective_price_threshold}
    """
    cursor.execute(query)
    
    # Fetch and print results
    results = cursor.fetchall()
    for row in results:
        print(row)
    
    # Close the database connection
    conn.close()

# Call the function to execute the script
get_orders()