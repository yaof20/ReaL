import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_301_database.db')
    cursor = conn.cursor()

    # Prompt the user for input
    campaign_name = input("Enter the campaign name: ")

    # Construct the SQL query
    query = f"SELECT * FROM marketing_campaigns WHERE campaign_name = '{campaign_name}'"

    # Execute the query
    cursor.execute(query)

    # Fetch all records from the query
    records = cursor.fetchall()

    # Print the results
    if records:
        print("Records found:")
        for row in records:
            print(row)
    else:
        print("No matching campaign found.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()