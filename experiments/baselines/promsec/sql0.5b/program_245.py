import sqlite3

def connect_to_database():
    conn = sqlite3.connect('program_245_database.db')
    return conn

def execute_query(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def display_inventory(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    inventory = cursor.fetchall()
    for item in inventory:
        print(item)

def main():
    conn = connect_to_database()
    query = input("Enter item name: ")
    supplier = input("Enter supplier name: ")
    min_quantity = input("Enter minimum quantity: ")

    # Execute the query to find items matching the criteria
    results = execute_query(conn, f"SELECT * FROM inventory WHERE item_name = ? AND supplier = ? AND quantity >= ?")

    # Display the results
    display_inventory(conn)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()