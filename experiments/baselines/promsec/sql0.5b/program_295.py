import sqlite3

def get_account_details(account_id, min_balance):
    # Connect to the database
    conn = sqlite3.connect('program_295_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT account_id, account_holder, balance FROM accounts WHERE account_id = ? AND balance >= ?"
    
    # Execute the query
    cursor.execute(query, (account_id, min_balance))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Print the results
    if results:
        for row in results:
            print(row)
    else:
        print("No matching records found.")

# Example usage
account_id = input("Enter account ID: ")
min_balance = input("Enter minimum balance: ")
get_account_details(account_id, min_balance)