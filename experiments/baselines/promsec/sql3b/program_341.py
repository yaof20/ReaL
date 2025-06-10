import sqlite3

# Connect to the database
conn = sqlite3.connect('program_341_database.db')
cursor = conn.cursor()

# Get user inputs
min_avg_score = float(input())
max_avg_score = float(input())
desired_position = input()
excluded_team = input()

# Build the SQL query
query = f"""
SELECT id, name, team, avg_score, position
FROM player_stats
WHERE avg_score BETWEEN {min_avg_score} AND {max_avg_score}
AND position = '{desired_position}'
AND team != '{excluded_team}'
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