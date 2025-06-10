import sqlite3

def get_transactions():
    # Connect to the database
    conn = sqlite3.connect('program_377_database.db')
    cursor = conn.cursor()
    
    # Prompt user for input
    min_amount = float(input("Enter minimum transaction amount: "))
    max_amount = float(input("Enter maximum transaction amount: "))
    category = input("Enter transaction category: ")
    
    # Construct SQL query based on user input
    query = f"SELECT * FROM transactions WHERE (amount BETWEEN {min_amount} AND {max_amount}) OR category = '{category}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Call the function
get_transactions()