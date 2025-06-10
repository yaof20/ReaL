import sqlite3

def fetch_account_details(account_number):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_437_database.db')
    cursor = conn.cursor()
    
    # SQL query to fetch account details
    query = f"SELECT holder_name, balance FROM accounts WHERE account_number = {account_number}"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the connection
    conn.close()
    
    # Print the result
    if result:
        print(f"Account {account_number}: {result[0]} - Balance: {result[1]}")
    else:
        print("Account not found.")

# Main function to handle user input
def main():
    # Prompt the user for input
    account_number = input("Enter the account number: ")
    
    # Call the function to fetch account details
    fetch_account_details(account_number)

if __name__ == "__main__":
    main()