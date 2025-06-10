import sqlite3

def get_transactions(account_number, min_amount):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_231_database.db')
    cursor = conn.cursor()
    
    # Define the SQL query
    query = """
    SELECT transaction_id, account_number, amount, transaction_date, description
    FROM transactions
    WHERE account_number = ? AND amount >= ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (account_number, min_amount))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the database connection
    conn.close()

# Example usage
account_number = input("Enter the account number: ")
min_amount = input("Enter the minimum transaction amount: ")
get_transactions(account_number, min_amount)