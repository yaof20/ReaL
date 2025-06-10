import sqlite3
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect('program_126_database.db')
cursor = conn.cursor()

# Get user inputs
upper_date_bound = input("Enter the upper date bound (YYYY-MM-DD): ")
quantity_increase = int(input("Enter the quantity increase value: "))
category = input("Enter the category: ")

# Calculate the date range
upper_date = datetime.strptime(upper_date_bound, '%Y-%m-%d')
lower_date = upper_date - timedelta(days=quantity_increase)
lower_date_bound = lower_date.strftime('%Y-%m-%d')

# Build the SQL query
query = f"SELECT * FROM sales WHERE category = ? AND date BETWEEN ? AND ?"

# Execute the query
cursor.execute(query, (category, lower_date_bound, upper_date_bound))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()