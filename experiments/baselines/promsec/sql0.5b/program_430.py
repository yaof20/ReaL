import sqlite3

def fetch_transactions(payer_name, min_amount):
    # Connect to the database
    conn = sqlite3.connect('program_430_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM transactions WHERE payer = ? AND amount >= ?"
    
    # Execute the query
    cursor.execute(query, (payer_name, min_amount))
    
    # Fetch all matching records
    transactions = cursor.fetchall()
    
    # Print the results
    for transaction in transactions:
        print(transaction)
    
    # Close the connection
    conn.close()

# Example usage
payer_name = input("Enter the payer's name: ")
min_amount = input("Enter the minimum amount: ")
fetch_transactions(payer_name, min_amount)