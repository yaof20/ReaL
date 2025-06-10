import sqlite3

def fetch_sales_by_customer(customer_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_170_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query to fetch sales records for the specified customer
    query = f"SELECT order_id, customer_name, item, amount FROM sales WHERE customer_name = ?"
    
    # Execute the query with the input customer name
    cursor.execute(query, (customer_name,))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for order_id, customer_name, item, amount in results:
        print(f"Order ID: {order_id}, Customer Name: {customer_name}, Item: {item}, Amount: {amount}")
    
    # Close the database connection
    conn.close()

# Example usage
customer_name = input("Enter the customer name: ")
fetch_sales_by_customer(customer_name)