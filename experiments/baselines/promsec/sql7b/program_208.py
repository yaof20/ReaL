import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_208_database.db')
cursor = conn.cursor()

# Prompt the user to input the title of a listing
title = input("Enter the title of the listing: ")

# Build the SQL query to retrieve records that match the given title
query = "SELECT * FROM listings WHERE title = ?"

# Execute the query with the user's input
cursor.execute(query, (title,))

# Fetch all matching records
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()