import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_89_database.db')
    cursor = conn.cursor()

    # Prompt the user for input
    field = input("Enter the field to search by (item_id, item_name, category): ")
    value = input("Enter the value to search for: ")

    # Construct the SQL query based on the input
    if field == 'item_id':
        query = f"SELECT * FROM inventory WHERE item_id = {value}"
    elif field == 'item_name':
        query = f"SELECT * FROM inventory WHERE item_name = '{value}'"
    elif field == 'category':
        query = f"SELECT * FROM inventory WHERE category = '{value}'"
    else:
        print("Invalid field. Please enter 'item_id', 'item_name', or 'category'.")
        return

    # Execute the query and print the results
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()