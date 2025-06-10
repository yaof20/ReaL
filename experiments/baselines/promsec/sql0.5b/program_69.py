import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_69_database.db')
    cursor = conn.cursor()

    # Get user inputs
    customer_name = input("Enter a customer name (exact or partial): ")
    product_name = input("Enter a product name: ")
    min_amount = float(input("Enter a minimum amount: "))

    # Construct the SQL query
    query = f"""
    SELECT *
    FROM orders
    WHERE customer_name LIKE '%{customer_name}%'
    AND product = '{product_name}'
    AND amount >= {min_amount * 1.1}
    """

    # Execute the query
    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()