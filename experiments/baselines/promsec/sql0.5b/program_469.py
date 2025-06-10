import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_469_database.db')
    cursor = conn.cursor()

    # Prompt the user for input
    item_name = input("Enter the item name to search for: ")

    # Construct the SQL query to find all orders where the item_name matches the user input
    query = f"SELECT order_id, customer_name, item_name, quantity, price FROM orders WHERE item_name = '{item_name}'"

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