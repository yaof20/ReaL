import sqlite3

def search_customers():
    # Connect to the database
    conn = sqlite3.connect('program_320_database.db')
    cursor = conn.cursor()

    # Get user inputs
    email = input("Enter email (leave blank for no filter): ")
    min_balance = float(input("Enter minimum balance: "))
    max_balance = float(input("Enter maximum balance: "))

    # Build the SQL query
    query = "SELECT customer_id, name, email, balance FROM customers"
    if email:
        query += f" WHERE email = '{email}'"
    if min_balance or max_balance:
        query += " AND balance BETWEEN ? AND ?"
        if min_balance:
            query += f" AND balance >= {min_balance}"
        if max_balance:
            query += f" AND balance <= {max_balance}"

    # Execute the query
    cursor.execute(query)
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the connection
    conn.close()

# Call the function
search_customers()