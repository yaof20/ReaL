import sqlite3

# Connect to the database
conn = sqlite3.connect('program_411_database.db')
cursor = conn.cursor()

# Get user inputs
campaign_id = int(input())
metric = input()
min_value = float(input())

# Construct the SQL query
query = f"SELECT name, {metric} FROM campaign_analytics WHERE campaign_id = {campaign_id} AND {metric} >= {min_value}"

# Execute the query
cursor.execute(query)

# Fetch the results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()