import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_485_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
occupation = input("Enter occupation: ")
region = input("Enter region: ")

# Construct the SQL query
query = f"SELECT * FROM census WHERE occupation = '{occupation}' AND region = '{region}'"

# Execute the query
cursor.execute(query)

# Fetch all results
results = cursor.fetchall()

# Print the results
print(results)

# Close the database connection
conn.close()