import sqlite3

# Connect to the database
conn = sqlite3.connect('program_356_database.db')
cursor = conn.cursor()

# Get user inputs
min_income = float(input())
age = int(input())
employment_status = input()
adjustment_factor = float(input())

# Adjust the minimum income
adjusted_min_income = min_income + adjustment_factor

# Build the SQL query
query = """
SELECT * FROM census_data
WHERE income >= ? OR age = ? OR employment_status = ?
"""

# Execute the query
cursor.execute(query, (adjusted_min_income, age, employment_status))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()