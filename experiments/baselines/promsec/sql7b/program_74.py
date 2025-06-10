import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_74_database.db')
cursor = conn.cursor()

# Prompt the user to input a category name
category_input = input("Enter a category name: ")

# Sanitize the input by replacing single quotes with two single quotes and removing semicolons
sanitized_input = category_input.replace("'", "''").replace(";", "")

# Build the SQL query
query = f"SELECT item_id, item_name, category, quantity, price FROM items WHERE category = '{sanitized_input}'"

# Execute the query
cursor.execute(query)

# Fetch all the records
records = cursor.fetchall()

# Print the records in a readable format
for record in records:
    print(f"ID: {record[0]}, Name: {record[1]}, Category: {record[2]}, Quantity: {record[3]}, Price: {record[4]:.1f}")

# Close the connection
conn.close()