import sqlite3

# Connect to the database
conn = sqlite3.connect('program_315_database.db')
cursor = conn.cursor()

# Prompt user for inputs
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")
min_audience_size = int(input("Enter minimum audience size: "))
conversion_ratio = float(input("Enter desired conversion ratio: "))

# Construct the SQL query
query = """
SELECT * FROM campaigns
WHERE start_date >= ? AND end_date <= ?
   OR audience_size > ?
   OR conversions >= ?
"""

# Execute the query with user inputs
cursor.execute(query, (start_date, end_date, min_audience_size, min_audience_size * conversion_ratio))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()