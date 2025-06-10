import sqlite3

def fetch_products(category, max_price, id_value, search_term, sort_column, sort_direction):
    # Connect to the database
    conn = sqlite3.connect('program_235_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"""
    SELECT id, name, category, price
    FROM products
    WHERE category = ? AND price <= ? AND id != ? AND name LIKE ?
    ORDER BY {sort_column} {sort_direction}
    """
    
    # Execute the query with the provided parameters
    cursor.execute(query, (category, max_price, id_value, f'%{search_term}%'))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return results

# Example usage
category = input("Enter the category: ")
max_price = float(input("Enter the maximum price: "))
id_value = int(input("Enter the ID value: "))
search_term = input("Enter the search term: ")
sort_column = input("Enter the column name to sort by: ")
sort_direction = input("Enter the sort direction (ASC or DESC): ")

# Call the function and print the results
results = fetch_products(category, max_price, id_value, search_term, sort_column, sort_direction)
print(results)