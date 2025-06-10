import sqlite3

def display_all_items():
    conn = sqlite3.connect('program_245_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    for item in items:
        print(item)
    conn.close()

def search_inventory():
    conn = sqlite3.connect('program_245_database.db')
    cursor = conn.cursor()
    
    item_name = input("Enter the item name: ")
    supplier = input("Enter the supplier's name: ")
    min_quantity = int(input("Enter the minimum quantity: "))
    
    query = f"SELECT * FROM inventory WHERE item_name = ? AND supplier = ? AND quantity >= ?"
    cursor.execute(query, (item_name, supplier, min_quantity))
    results = cursor.fetchall()
    
    for result in results:
        print(result)
    
    conn.close()

if __name__ == "__main__":
    display_all_items()
    search_inventory()