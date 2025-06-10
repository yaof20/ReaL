import sqlite3

def get_transactions(min_amount, max_amount, category):
    # Connect to the database
    conn = sqlite3.connect('program_377_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM transactions WHERE amount BETWEEN {min_amount} AND {max_amount} OR category = '{category}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Example usage
min_amount = float(input("Enter the minimum transaction amount: "))
max_amount = float(input("Enter the maximum transaction amount: "))
category = input("Enter the transaction category: ")

get_transactions(min_amount, max_amount, category)