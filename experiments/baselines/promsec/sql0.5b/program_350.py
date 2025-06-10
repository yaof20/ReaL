import sqlite3

def get_customer_records(customer_name, min_balance):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_350_database.db')
    cursor = conn.cursor()
    
    # SQL query to retrieve customer records
    query = f"SELECT customer_id, name, email, balance FROM customers WHERE name = ? AND balance > ?"
    
    # Execute the query with the provided inputs
    cursor.execute(query, (customer_name, min_balance))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(f"({row[0]}, '{row[1]}', '{row[2]}', {row[3]})")
    
    # Close the database connection
    conn.close()

# Example usage
customer_name = input("Enter the customer name: ")
min_balance = float(input("Enter the minimum balance: "))
get_customer_records(customer_name, min_balance)