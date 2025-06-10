import sqlite3

def query_orders():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_69_database.db')
    cursor = conn.cursor()
    
    # Get user inputs
    customer_name = input("Enter customer name (exact or partial): ")
    product = input("Enter product name: ")
    min_amount = float(input("Enter minimum amount: "))
    
    # Calculate 90% of the minimum amount
    min_amount_90 = min_amount * 0.9
    
    # Construct the SQL query
    query = f"""
    SELECT order_id, customer_name, product, amount
    FROM orders
    WHERE customer_name LIKE ? AND product = ? AND amount >= ?
    """
    
    # Execute the query
    cursor.execute(query, (customer_name, product, min_amount_90))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the database connection
    conn.close()

# Call the function
query_orders()