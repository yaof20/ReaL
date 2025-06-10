import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_181_database.db')
cursor = conn.cursor()

# Prompt user for inputs
team_name = input("Enter team name: ")
position = input("Enter player position: ")
min_average = float(input("Enter minimum average: "))
sort_column = input("Enter column to sort by (name, team, position, average): ")
sort_order = input("Enter sorting order (ASC, DESC): ")

# Construct the SQL query
query = f"""
SELECT * FROM players
WHERE team = ? AND position = ? AND average >= ?
ORDER BY {sort_column} {sort_order}
"""

# Execute the query
cursor.execute(query, (team_name, position, min_average))

# Fetch all results
results = cursor.fetchall()

# Print each resulting row
for row in results:
    print(row)

# Close the database connection
conn.close()