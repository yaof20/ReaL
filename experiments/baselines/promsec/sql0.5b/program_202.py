import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_202_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    phone_number = input("Enter the phone number: ")
    minimum_amount_due = input("Enter the minimum amount due: ")

    # Construct the SQL query
    query = f"SELECT * FROM customer_bills WHERE phone = ? AND amount_due > ?"

    # Execute the query
    cursor.execute(query, (phone_number, minimum_amount_due))

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()