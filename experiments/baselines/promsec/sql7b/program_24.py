import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_24_database.db')
cursor = conn.cursor()

# Prompt user for inputs
min_age = int(input("Enter minimum age: "))
max_age = int(input("Enter maximum age: "))
target_city = input("Enter target city: ")
include_younger_than_min = input("Include customers younger than the minimum age? (yes/no): ").lower()

# Construct the SQL query based on user inputs
query = "SELECT * FROM customers WHERE age BETWEEN ? AND ? AND city = ?"
params = (min_age, max_age, target_city)

# If the user wants to include customers younger than the minimum age, adjust the query
if include_younger_than_min == 'yes':
    query = "SELECT * FROM customers WHERE age >= ? AND city = ?"
    params = (min_age, target_city)

# Execute the query
cursor.execute(query, params)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()