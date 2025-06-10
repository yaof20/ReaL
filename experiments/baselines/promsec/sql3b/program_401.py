import sqlite3

# Connect to the database
conn = sqlite3.connect('program_401_database.db')
cursor = conn.cursor()

# Prompt the user for input
title = input("Enter the book title: ")
author = input("Enter the author name: ")

# Construct the SQL query
query = f"SELECT * FROM books WHERE title = ? AND author = ?"

# Execute the query
cursor.execute(query, (title, author))

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()