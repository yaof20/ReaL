import sqlite3

# Connect to the database
conn = sqlite3.connect('program_345_database.db')
cursor = conn.cursor()

# Prompt user for inputs
year_published = input("Enter the publication year: ")
category = input("Enter the research category: ")

# Build SQL query
query = "SELECT * FROM papers WHERE year_published = ? AND category = ?"

# Execute query
cursor.execute(query, (year_published, category))

# Fetch and print results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()