import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_197_database.db')
    cursor = conn.cursor()

    # Prompt the user for input
    start_date = input("Enter the start date in 'YYYY-MM-DD' format: ")
    end_date = input("Enter the end date in 'YYYY-MM-DD' format: ")

    # Construct the SQL query
    query = f"SELECT transaction_id, product_name, quantity, price_per_unit, sale_date FROM sales_data WHERE sale_date BETWEEN '{start_date}' AND '{end_date}'"

    # Execute the query
    cursor.execute(query)

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()