import sqlite3

def get_orders(min_price, max_price, category):
    # Connect to the database
    conn = sqlite3.connect('program_248_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM orders WHERE price BETWEEN {min_price} AND {max_price} AND category = '{category}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return results

# Get user inputs
min_price = float(input("Enter the minimum price: "))
max_price = float(input("Enter the maximum price: "))
category = input("Enter the category: ")

# Get the orders
orders = get_orders(min_price, max_price, category)

# Print the results
print(orders)