import sqlite3

def retrieve_orders_by_customer_name():
    # Connect to the database
    conn = sqlite3.connect('program_1_database.db')
    cursor = conn.cursor()
    
    # Get user input
    customer_name = input("Enter the customer's name: ")
    
    # Construct the SQL query
    query = f"SELECT * FROM orders WHERE customer_name = '{customer_name}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all rows from the result
    rows = cursor.fetchall()
    
    # Print each row
    for row in rows:
        print(row)
    
    # Close the connection
    conn.close()

# Call the function
retrieve_orders_by_customer_name()