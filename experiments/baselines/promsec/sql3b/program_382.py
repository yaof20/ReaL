import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_382_database.db')
cursor = conn.cursor()

# Prompt user for inputs
min_age = int(input("Enter the minimum age: "))
country = input("Enter the country: ")
keyword = input("Enter the keyword to search in the bio: ")

# Construct the SQL query based on user inputs
query = f"""
SELECT user_id, username, email, bio, age, country
FROM users
WHERE age >= {min_age}
  OR country = '{country}'
  OR bio LIKE '%{keyword}%';
"""

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()