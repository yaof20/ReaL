import sqlite3

def get_orders_by_customer_name(customer_name):
    # Connect to the database
    conn = sqlite3.connect('program_1_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM orders WHERE customer_name = ?"
    
    # Execute the query with the user-provided input
    cursor.execute(query, (customer_name,))
    
    # Fetch all the rows from the query
    rows = cursor.fetchall()
    
    # Print each row of the result
    for row in rows:
        print(row)
    
    # Close the database connection
    conn.close()

# Example usage
customer_name = input("Enter the customer's name: ")
get_orders_by_customer_name(customer_name)