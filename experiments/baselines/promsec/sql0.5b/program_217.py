import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_217_database.db')
    cursor = conn.cursor()

    # Prompt the user for input
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    min_amount_due = float(input("Enter the minimum amount due (a number): "))
    payment_status = input("Enter the payment status (Pending or Paid): ")

    # Construct the SQL query
    query = f"""
    SELECT id, customer_name, billing_date, amount_due, status
    FROM billing
    WHERE billing_date BETWEEN '{start_date}' AND '{end_date}'
    AND amount_due >= {min_amount_due}
    AND status = '{payment_status}'
    """

    # Execute the query
    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    print(results)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()