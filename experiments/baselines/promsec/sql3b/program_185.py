import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_185_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
location = input("Enter the location: ")
event_date = input("Enter the event date (YYYY-MM-DD): ")
ticket_amount = int(input("Enter the ticket amount: "))

# Construct the SQL query
query = """
SELECT event_id, title, date, location, available_tickets
FROM events
WHERE location = ? AND date = ? AND available_tickets >= ?
"""

# Execute the query with user inputs
cursor.execute(query, (location, event_date, ticket_amount))

# Fetch all results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()