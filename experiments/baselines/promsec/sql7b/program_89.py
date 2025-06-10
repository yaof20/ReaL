import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_89_database.db')
cursor = conn.cursor()

# Prompt user for the field to search by
search_field = input("Enter the field to search by (item_id, item_name, category): ")

# Validate the search field
if search_field not in ['item_id', 'item_name', 'category']:
    print("Invalid field. Please choose from item_id, item_name, or category.")
else:
    # Prompt user for the value to search for
    search_value = input(f"Enter the value to search for in {search_field}: ")

    # Construct the SQL query
    query = f"SELECT * FROM inventory WHERE {search_field} = ?"

    try:
        # Execute the query
        cursor.execute(query, (search_value,))
        # Fetch all matching rows
        results = cursor.fetchall()
        # Print the results
        for row in results:
            print(row)
    except sqlite3.Error as e:
        # Handle any errors that occur during query execution
        print(f"An error occurred: {e}")

# Close the database connection
conn.close()