import sqlite3

def fetch_customer_orders():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_170_database.db')
    cursor = conn.cursor()
    
    # Prompt the user to input a customer name
    customer_name = input("Enter the customer name: ")
    
    # Construct the SQL query to fetch orders for the specified customer
    query = f"SELECT order_id, customer_name, item, amount FROM sales WHERE customer_name = ?"
    
    # Execute the query with the user's input
    cursor.execute(query, (customer_name,))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the database connection
    conn.close()

# Call the function to execute the task
fetch_customer_orders()