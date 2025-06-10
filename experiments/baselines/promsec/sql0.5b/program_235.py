import sqlite3

def get_products_by_category(category, max_price, id_value, search_term, column_name, sort_direction):
    # Connect to the database
    conn = sqlite3.connect('program_235_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM products WHERE category = ? AND price <= ? AND id = ? AND name LIKE ? ORDER BY {column_name} {sort_direction}"
    
    # Execute the query
    cursor.execute(query, (category, max_price, id_value, search_term))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Example usage
get_products_by_category('Clothing', 100, 8, 'jacket', 'id', 'DESC')
get_products_by_category('Clothing', 100, 4, 'sneakers', 'category', 'ASC')