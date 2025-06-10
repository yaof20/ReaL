import sqlite3

def get_products_by_department_and_cost(department, max_cost):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_308_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT product_id, product_name, department, cost FROM products WHERE department = ? AND cost <= ?"
    
    # Execute the query
    cursor.execute(query, (department, max_cost))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for product in results:
        print(product)
    
    # Close the connection
    conn.close()

# Example usage
department = input("Enter the department name: ")
max_cost = float(input("Enter the maximum cost: "))
get_products_by_department_and_cost(department, max_cost)