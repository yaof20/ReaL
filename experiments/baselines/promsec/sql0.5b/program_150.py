import sqlite3

def get_orders_by_customer(customer_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_150_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query to retrieve orders by customer
    query = f"SELECT order_id, product_name, customer, shipping_address, status FROM orders WHERE customer = ?"
    
    # Execute the query with the input customer name
    cursor.execute(query, (customer_name,))
    
    # Fetch all the results
    orders = cursor.fetchall()
    
    # Print the results
    for order in orders:
        print(order)
    
    # Close the database connection
    conn.close()

# Example usage
customer_name = input("Enter a customer name: ")
get_orders_by_customer(customer_name)