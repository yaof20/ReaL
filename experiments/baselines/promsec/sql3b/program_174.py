import sqlite3

# Connect to the database
conn = sqlite3.connect('program_174_database.db')
cursor = conn.cursor()

# Get the researcher's name from the user
researcher_name = input("Enter the researcher's name: ")

# Construct the SQL query to retrieve data for the specific researcher
query = f"SELECT * FROM studies WHERE researcher = '{researcher_name}'"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()