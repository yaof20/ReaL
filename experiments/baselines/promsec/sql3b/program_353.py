import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_353_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
room_type = input("Enter the room type: ")
check_in_date = input("Enter the check-in date (YYYY-MM-DD): ")
check_out_date = input("Enter the check-out date (YYYY-MM-DD): ")
max_price = float(input("Enter the maximum price: "))

# Construct the SQL query based on user inputs
query = f"""
SELECT reservation_id, guest_name, room_type, check_in_date, check_out_date, price
FROM reservations
WHERE room_type = '{room_type}'
  AND check_in_date >= '{check_in_date}'
  AND check_out_date <= '{check_out_date}'
  AND price <= {max_price}
"""

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()