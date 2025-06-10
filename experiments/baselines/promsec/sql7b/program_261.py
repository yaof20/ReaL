import sqlite3

# Connect to the database
conn = sqlite3.connect('program_261_database.db')
cursor = conn.cursor()

# Get user inputs
min_price = float(input())
max_price = float(input())
discount_percentage = float(input())
location = input()

# Calculate the discounted price range
discounted_min_price = min_price * (1 - discount_percentage)
discounted_max_price = max_price * (1 - discount_percentage)

# Build the SQL query
query = f"SELECT * FROM tickets WHERE location = ? AND ticket_price BETWEEN ? AND ?"

# Execute the query
cursor.execute(query, (location, discounted_min_price, discounted_max_price))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()