import sqlite3

# Connect to the database
conn = sqlite3.connect('program_215_database.db')
cursor = conn.cursor()

# Get user inputs
min_friends = int(input())
max_friends = int(input())
age_preference = int(input())
keyword = input()

# Adjust the friends_count range
min_friends -= 10
max_friends += 10

# Build the SQL query
query = f"SELECT * FROM users WHERE friends_count BETWEEN {min_friends} AND {max_friends} AND (age = {age_preference} OR bio LIKE '%{keyword}%')"

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()