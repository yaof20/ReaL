import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_308_database.db')
cursor = conn.cursor()

# Prompt the user for input
department = input("Enter the department name: ")
max_cost = float(input("Enter the maximum cost: "))

# Build the SQL query
query = f"SELECT product_id, product_name, department, cost FROM products WHERE department = ? AND cost <= ?"

# Execute the query
cursor.execute(query, (department, max_cost))

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()