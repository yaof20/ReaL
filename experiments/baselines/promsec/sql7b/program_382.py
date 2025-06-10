import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_382_database.db')
cursor = conn.cursor()

# Prompt user for inputs
min_age = int(input("Enter minimum age: "))
country = input("Enter country: ")
keyword = input("Enter keyword to search in bio: ")

# Construct the SQL query
query = """
SELECT * FROM users
WHERE age >= ? OR country = ? OR bio LIKE ?
"""

# Execute the query with user inputs
cursor.execute(query, (min_age, country, f'%{keyword}%'))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()