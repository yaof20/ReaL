import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_442_database.db')
cursor = conn.cursor()

# Prompt user for inputs
name = input("Enter player's name: ")
team = input("Enter team name: ")
points = int(input("Enter points to filter by: "))
display_column = input("Enter column to display: ")
order_direction = input("Enter order direction (ASC or DESC): ")

# Construct the SQL query
query = f"SELECT {display_column} FROM players WHERE name = ? OR team = ? OR points > ? ORDER BY {display_column} {order_direction}"

# Execute the query
cursor.execute(query, (name, team, points))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()