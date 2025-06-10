import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_233_database.db')
cursor = conn.cursor()

# Prompt user for inputs
event_location = input("Enter event location: ")
earliest_date = input("Enter earliest date (YYYY-MM-DD): ")
latest_date = input("Enter latest date (YYYY-MM-DD): ")

# Build SQL query based on user inputs
query = """
SELECT * FROM events
WHERE location = ? AND date BETWEEN ? AND ?
"""

# Execute the query
cursor.execute(query, (event_location, earliest_date, latest_date))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()