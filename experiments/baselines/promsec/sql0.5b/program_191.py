import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_191_database.db')
    cursor = conn.cursor()

    # Get user inputs
    customer_name = input("Enter the customer name: ")
    min_quantity = int(input("Enter the minimum quantity to filter orders: "))
    dish_type_preference = input("Enter the dish type preference: ")
    price_limit = float(input("Enter the price limit to filter orders: "))

    # Construct the SQL query
    query = f"""
    SELECT order_id, customer_name, dish, quantity, price
    FROM orders
    WHERE customer_name = '{customer_name}'
    AND (quantity >= {min_quantity} OR dish = '{dish_type_preference}' OR price <= {price_limit})
    """

    # Execute the query
    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    for order in results:
        print(order)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()