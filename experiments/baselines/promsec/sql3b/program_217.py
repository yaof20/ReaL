import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_217_database.db')
    cursor = conn.cursor()

    # Prompt user for inputs
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    min_amount = float(input("Enter minimum amount due: "))
    payment_status = input("Enter payment status (Pending or Paid): ")

    # Build the SQL query
    query = f"""
    SELECT * FROM billing
    WHERE billing_date BETWEEN '{start_date}' AND '{end_date}'
    AND amount_due >= {min_amount}
    AND status = '{payment_status}'
    """

    # Execute the query
    cursor.execute(query)

    # Fetch all results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()