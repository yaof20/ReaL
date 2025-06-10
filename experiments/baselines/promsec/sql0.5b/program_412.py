import sqlite3

def get_products_by_category_and_price(category, min_price, max_price):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_412_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM products WHERE category = ? AND price BETWEEN ? AND ?"
    
    # Execute the query with the provided inputs
    cursor.execute(query, (category, min_price, max_price))
    
    # Fetch all the products
    products = cursor.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Print the results
    if products:
        print("Products matching the criteria:")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Category: {product[2]}, Price: {product[3]}")
    else:
        print("No products found matching the criteria.")

# Example usage
get_products_by_category_and_price('Kitchen', 5, 15)
get_products_by_category_and_price('Electronics', 50, 150)