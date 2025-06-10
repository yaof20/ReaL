import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_24_database.db')
cursor = conn.cursor()

# Prompt the user for input
min_age = int(input("Enter the minimum age: "))
max_age = int(input("Enter the maximum age: "))
city = input("Enter the target city: ")
include_younger_than_min = input("Do you want to include customers younger than the minimum age? (yes/no): ").strip().lower() == 'yes'

# Construct the SQL query based on the user's input
query = f"SELECT customer_id, first_name, last_name, age, city FROM customers WHERE age BETWEEN {min_age} AND {max_age} AND city = '{city}'"
if include_younger_than_min:
    query += " OR age < {min_age}"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()