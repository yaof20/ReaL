import sqlite3

# Connect to the database
conn = sqlite3.connect('program_345_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
year_published = input("Enter the publication year: ")
category = input("Enter the research category: ")

# Build the SQL query
query = f"SELECT * FROM papers WHERE year_published = {year_published} AND category = '{category}'"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()