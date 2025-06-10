import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_424_database.db')
cursor = conn.cursor()

# Prompt user for inputs
search_field = input("Enter the search field (first_name, last_name, email, phone): ")
search_value = input("Enter the search value: ")
sort_field = input("Enter the field to sort by (customer_id, first_name, last_name, email, phone): ")
order_direction = input("Enter the order direction (ASC or DESC): ")

# Construct the SQL query
query = f"SELECT * FROM customers WHERE {search_field} = ? ORDER BY {sort_field} {order_direction}"

# Execute the query
cursor.execute(query, (search_value,))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()