import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_208_database.db')
cursor = conn.cursor()

# Prompt the user to input the title of a listing
title = input("Enter the title of the listing: ")

# Construct the SQL query to retrieve records with the given title
query = f"SELECT * FROM listings WHERE title = '{title}'"

# Execute the query
cursor.execute(query)

# Fetch all the records that match the given title
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()