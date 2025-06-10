import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_485_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
occupation = input("Enter occupation: ")
region = input("Enter region: ")

# Construct the SQL query
query = f"SELECT * FROM census WHERE occupation = ? AND region = ?"

# Execute the query
cursor.execute(query, (occupation, region))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()