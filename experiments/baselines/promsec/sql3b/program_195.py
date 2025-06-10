import sqlite3

# Connect to the database
conn = sqlite3.connect('program_195_database.db')
cursor = conn.cursor()

# Get user inputs
author = input("Enter the author's name: ")
start_date = input("Enter the start publish date (YYYY-MM-DD): ")
end_date = input("Enter the end publish date (YYYY-MM-DD): ")
keyword = input("Enter the keyword: ")

# Build the SQL query
query = """
SELECT post_id, title, content, author, publish_date
FROM posts
WHERE author = ? AND publish_date BETWEEN ? AND ? AND (title LIKE ? OR content LIKE ?)
"""

# Execute the query with user inputs
cursor.execute(query, (author, start_date, end_date, f'%{keyword}%', f'%{keyword}%'))

# Fetch all results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()