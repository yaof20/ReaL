import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_181_database.db')
cursor = conn.cursor()

# Prompt user for inputs
team_name = input("Enter team name: ")
player_position = input("Enter player position: ")
min_average = float(input("Enter minimum average: "))
sort_column = input("Enter column to sort by (name, team, position, average): ")
sort_order = input("Enter sorting order (ASC or DESC): ")

# Construct the SQL query
query = f"SELECT * FROM players WHERE team = ? AND position = ? AND average >= ? ORDER BY {sort_column} {sort_order}"

# Execute the query
cursor.execute(query, (team_name, player_position, min_average))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()