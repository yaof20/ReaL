import sqlite3

# Connect to the database
conn = sqlite3.connect('program_174_database.db')
cursor = conn.cursor()

# Get the researcher's name from the user
researcher_name = input("Enter the researcher's name: ")

# Build the SQL query
query = "SELECT * FROM studies WHERE researcher = ?"

# Execute the query
cursor.execute(query, (researcher_name,))

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()