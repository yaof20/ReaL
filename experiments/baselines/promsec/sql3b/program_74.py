import sqlite3

def sanitize_input(input_str):
    # Replace single quotes with two single quotes
    sanitized_str = input_str.replace("'", "''")
    # Remove semicolons
    sanitized_str = sanitized_str.replace(';', '')
    return sanitized_str

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_74_database.db')
    cursor = conn.cursor()
    
    # Prompt the user to input a category name
    category = input("Enter a category name: ")
    
    # Sanitize the user input
    sanitized_category = sanitize_input(category)
    
    # Construct the SQL query
    query = f"SELECT item_id, item_name, category, quantity, price FROM items WHERE category = '{sanitized_category}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the records
    records = cursor.fetchall()
    
    # Print the results
    if records:
        for record in records:
            print(f"ID: {record[0]}, Name: {record[1]}, Category: {record[2]}, Quantity: {record[3]}, Price: {record[4]}")
    else:
        print("No records found for the given category.")
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()