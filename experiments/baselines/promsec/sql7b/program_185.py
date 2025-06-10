import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_185_database.db')
cursor = conn.cursor()

# Prompt user for inputs
location = input("Enter location: ")
event_date = input("Enter event date (YYYY-MM-DD): ")
ticket_amount = int(input("Enter ticket amount: "))

# Construct SQL query
query = """
SELECT * FROM events
WHERE location = ? AND date = ? AND available_tickets >= ?
"""

# Execute the query
cursor.execute(query, (location, event_date, ticket_amount))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()