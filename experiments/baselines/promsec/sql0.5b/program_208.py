import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_208_database.db')
cursor = conn.cursor()

# Prompt the user for input
title = input("Enter the title of the listing: ")

# Construct the SQL query to fetch records from the 'listings' table
query = f"SELECT * FROM listings WHERE title = '{title}'"

# Execute the query
cursor.execute(query)

# Fetch all records from the query
records = cursor.fetchall()

# Print the results
for record in records:
    print(record)

# Close the database connection
conn.close()