import sqlite3

def get_products_by_category_and_price(category, min_price, max_price):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_412_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = """
    SELECT * FROM products
    WHERE category = ? AND price BETWEEN ? AND ?
    """
    
    # Execute the query with the user inputs
    cursor.execute(query, (category, min_price, max_price))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Close the database connection
    conn.close()
    
    return results

# Prompt the user for input
category = input("Enter the category name: ")
min_price = float(input("Enter the minimum price: "))
max_price = float(input("Enter the maximum price: "))

# Get the products that match the criteria
products = get_products_by_category_and_price(category, min_price, max_price)

# Print the results
print(products)