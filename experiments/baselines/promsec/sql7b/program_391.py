import sqlite3

# Connect to the database
conn = sqlite3.connect('program_391_database.db')
cursor = conn.cursor()

# Get user inputs
city = input("Enter city name: ")
min_age = int(input("Enter minimum age: "))
min_income = float(input("Enter minimum income: "))

# Build the SQL query
query = """
SELECT * FROM census_data
WHERE city = ? AND (age >= ? OR income >= ?)
"""

# Execute the query
cursor.execute(query, (city, min_age, min_income))

# Fetch all results
results = cursor.fetchall()

# Print the results
print(results)

# Close the connection
conn.close()