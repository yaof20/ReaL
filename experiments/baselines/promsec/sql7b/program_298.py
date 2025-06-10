import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_298_database.db')
cursor = conn.cursor()

# Prompt user for inputs
start_year = int(input("Enter the starting publication year: "))
end_year = int(input("Enter the ending publication year: "))
genre = input("Enter the genre: ")
author_substring = input("Enter the author's name substring: ")

# Construct the SQL query
query = """
SELECT * FROM books
WHERE year BETWEEN ? AND ?
AND genre = ?
AND author LIKE ?
"""

# Execute the query with user inputs
cursor.execute(query, (start_year, end_year, genre, f'%{author_substring}%'))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()