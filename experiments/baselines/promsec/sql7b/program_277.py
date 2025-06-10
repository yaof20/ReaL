import sqlite3

# Connect to the database
conn = sqlite3.connect('program_277_database.db')
cursor = conn.cursor()

# Get user inputs
event_name = input("Enter the event name (or 'all' to match any event): ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
location = input("Enter the location: ")

# Build the SQL query
query = "SELECT * FROM tickets WHERE 1=1"
if event_name != 'all':
    query += f" AND event_name = '{event_name}'"
if start_date:
    query += f" AND date >= '{start_date}'"
if end_date:
    query += f" AND date <= '{end_date}'"
if location:
    query += f" AND location = '{location}'"

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()