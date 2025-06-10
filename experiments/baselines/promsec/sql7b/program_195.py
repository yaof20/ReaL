import sqlite3

# Connect to the database
conn = sqlite3.connect('program_195_database.db')
cursor = conn.cursor()

# Get user inputs
author_name = input("Enter author's name: ")
start_date = input("Enter start publish date (YYYY-MM-DD): ")
end_date = input("Enter end publish date (YYYY-MM-DD): ")
keyword = input("Enter keyword: ")

# Build SQL query
query = """
SELECT * FROM posts
WHERE author = ? AND publish_date BETWEEN ? AND ? AND (title LIKE ? OR content LIKE ?)
"""

# Execute the query
cursor.execute(query, (author_name, start_date, end_date, f'%{keyword}%', f'%{keyword}%'))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()