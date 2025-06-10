import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_171_database.db')
cursor = conn.cursor()

# Prompt user for inputs
department = input("Enter the department name to filter by: ")
order_column = input("Enter the column name to order by: ")
order_direction = input("Enter the order direction (ASC or DESC): ")

# Construct the SQL query
query = f"SELECT emp_id, first_name, last_name FROM employees WHERE department = ? ORDER BY ? {order_direction}"

try:
    # Execute the query
    cursor.execute(query, (department,))
    
    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(f"{row[0]} {row[1]} {row[2]}")
except sqlite3.Error as e:
    # Handle exceptions
    print(f"An error occurred: {e}")

# Close the connection
conn.close()