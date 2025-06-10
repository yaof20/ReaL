import sqlite3

# Connect to the database
conn = sqlite3.connect('program_407_database.db')
cursor = conn.cursor()

# Get user inputs
min_price = float(input())
max_price = float(input())
event_date = input()
event_name_substring = input()

# Construct the SQL query
query = """
SELECT * FROM tickets
WHERE price BETWEEN ? AND ?
AND date = ?
AND event_name LIKE ?
"""

# Execute the query
cursor.execute(query, (min_price, max_price, event_date, f'%{event_name_substring}%'))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()