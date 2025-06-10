import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_372_database.db')
cursor = conn.cursor()

# Get user inputs
doctor_name = input("Enter doctor's name: ")
min_age = int(input("Enter minimum age: "))
max_age = int(input("Enter maximum age: "))
search_field = input("Enter search field (name, diagnosis, treatment): ")
search_value = input("Enter search value: ")
order_column = input("Enter column to order by (patient_id, name, age): ")
order_direction = input("Enter order direction (ASC or DESC): ")

# Construct the SQL query
query = f"SELECT * FROM patients WHERE doctor = ? AND age BETWEEN ? AND ? AND {search_field} = ? ORDER BY {order_column} {order_direction}"

# Execute the query
cursor.execute(query, (doctor_name, min_age, max_age, search_value))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()