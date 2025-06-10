import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_74_database.db')
cursor = conn.cursor()

# Prompt the user for input
category_input = input("Enter a category name (e.g., Appliances, Electronics): ")

# Sanitize the input by replacing single quotes with two single quotes and removing semicolons
sanitized_category_input = category_input.replace("'", "''").replace(";", "")

# Construct the SQL query
query = f"SELECT item_id, item_name, category, quantity, price FROM items WHERE category = '{sanitized_category_input}'"

# Execute the query
cursor.execute(query)

# Fetch all records from the query
records = cursor.fetchall()

# Print each record in a readable format
for record in records:
    print(f"ID: {record[0]}, Name: {record[1]}, Category: {record[2]}, Quantity: {record[3]}, Price: {record[4]}")

# Close the database connection
conn.close()