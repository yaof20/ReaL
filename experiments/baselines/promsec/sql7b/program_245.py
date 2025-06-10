import sqlite3

def search_inventory(item_name, supplier, min_quantity):
    conn = sqlite3.connect('program_245_database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM inventory WHERE item_name = ? AND supplier = ? AND quantity >= ?"
    cursor.execute(query, (item_name, supplier, min_quantity))
    results = cursor.fetchall()
    for row in results:
        print(row)
    conn.close()

def display_inventory():
    conn = sqlite3.connect('program_245_database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM inventory"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)
    conn.close()

if __name__ == "__main__":
    item_name = input("Enter item name: ")
    supplier = input("Enter supplier name: ")
    min_quantity = int(input("Enter minimum quantity: "))
    search_inventory(item_name, supplier, min_quantity)
    display_inventory()