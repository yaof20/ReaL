import sqlite3

# Connect to the database
conn = sqlite3.connect('program_407_database.db')
cursor = conn.cursor()

# Get user inputs
min_price = float(input("Enter the minimum ticket price: "))
max_price = float(input("Enter the maximum ticket price: "))
event_date = input("Enter the event date (YYYY-MM-DD): ")
event_name = input("Enter the part of the event name: ")

# Construct the SQL query
query = f"""
SELECT ticket_id, event_name, date, price
FROM tickets
WHERE price BETWEEN {min_price} AND {max_price}
AND date = '{event_date}'
AND event_name LIKE '%{event_name}%';
"""

# Execute the query
cursor.execute(query)

# Fetch all results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the connection
conn.close()