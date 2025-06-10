import sqlite3

# Connect to the database
conn = sqlite3.connect('program_341_database.db')
cursor = conn.cursor()

# Get user inputs
min_score = float(input())
max_score = float(input())
position = input()
exclude_team = input()

# Build the SQL query
query = f"SELECT * FROM player_stats WHERE avg_score BETWEEN {min_score} AND {max_score} AND position = ? AND team != ?"

# Execute the query
cursor.execute(query, (position, exclude_team))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()