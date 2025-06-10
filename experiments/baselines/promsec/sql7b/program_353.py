import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_353_database.db')
cursor = conn.cursor()

# Prompt user for inputs
room_type = input("Enter room type (Single, Double, Suite): ")
check_in_date = input("Enter check-in date (YYYY-MM-DD): ")
check_out_date = input("Enter check-out date (YYYY-MM-DD): ")
max_price = float(input("Enter maximum price: "))

# Construct the SQL query
query = """
SELECT * FROM reservations
WHERE room_type = ? AND
      (check_in_date <= ? AND check_out_date >= ?) OR
      price <= ?
"""

# Execute the query
cursor.execute(query, (room_type, check_in_date, check_out_date, max_price))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()