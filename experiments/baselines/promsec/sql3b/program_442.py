import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_442_database.db')
cursor = conn.cursor()

# Prompt user for inputs
player_name = input("Enter player's name: ")
team_name = input("Enter team name: ")
points = int(input("Enter points to filter by: "))
column_to_display = input("Enter the column to display: ")
order_direction = input("Enter the order direction (ASC or DESC): ")

# Construct the SQL query
query = f"""
SELECT {column_to_display}
FROM players
WHERE name = ? OR team = ? OR points > ?
ORDER BY {column_to_display} {order_direction}
"""

# Execute the query
cursor.execute(query, (player_name, team_name, points))

# Fetch all results
results = cursor.fetchall()

# Print the results
print(results)

# Close the database connection
conn.close()