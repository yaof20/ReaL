import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_77_database.db')
    cursor = conn.cursor()

    # Prompt the user to input an item type
    item_type = input("Enter an item type to search for: ")

    # Construct the SQL query to retrieve all records from the 'inventory' table where the 'item_type' matches the user's input
    query = f"SELECT * FROM inventory WHERE item_type = '{item_type}'"

    # Execute the SQL query
    cursor.execute(query)

    # Fetch all the records from the query
    records = cursor.fetchall()

    # Print the results
    for record in records:
        print(record)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()