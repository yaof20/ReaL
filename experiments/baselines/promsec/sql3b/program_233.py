import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_233_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
event_location = input("Enter the event location: ")
earliest_date = input("Enter the earliest date (YYYY-MM-DD): ")
latest_date = input("Enter the latest date (YYYY-MM-DD): ")

# Build the SQL query
query = """
SELECT id, event_name, location, date
FROM events
WHERE location = ? AND date BETWEEN ? AND ?
"""

# Execute the query with user inputs
cursor.execute(query, (event_location, earliest_date, latest_date))

# Fetch all results
results = cursor.fetchall()

# Print the results
print(results)

# Close the database connection
conn.close()