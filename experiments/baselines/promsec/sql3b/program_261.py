import sqlite3

# Connect to the database
conn = sqlite3.connect('program_261_database.db')
cursor = conn.cursor()

# Get user inputs
min_price = float(input("Enter the minimum ticket price: "))
max_price = float(input("Enter the maximum ticket price: "))
discount_percentage = float(input("Enter the ticket discount percentage: "))
location = input("Enter the desired event location: ")

# Calculate the adjusted price range
adjusted_min_price = min_price * (1 - discount_percentage)
adjusted_max_price = max_price * (1 - discount_percentage)

# Construct the SQL query
query = f"""
SELECT event_id, event_name, location, ticket_price
FROM tickets
WHERE location = ? AND ticket_price BETWEEN ? AND ?
"""

# Execute the query
cursor.execute(query, (location, adjusted_min_price, adjusted_max_price))

# Fetch the results
results = cursor.fetchall()

# Print the results
print(results)

# Close the connection
conn.close()