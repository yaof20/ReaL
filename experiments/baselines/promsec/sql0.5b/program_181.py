import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_181_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    team_name = input("Enter the team name: ")
    player_position = input("Enter the player position: ")
    min_average = float(input("Enter the minimum average: "))
    column_to_sort_by = input("Enter the column to sort by (name, team, position, average): ")
    sort_order = input("Enter the sorting order (ASC or DESC): ")

    # Construct the SQL query
    query = f"SELECT * FROM players WHERE team = ? AND position = ? AND average >= ? AND {column_to_sort_by} = ? ORDER BY {column_to_sort_by} {sort_order}"

    # Execute the query
    cursor.execute(query, (team_name, player_position, min_average, column_to_sort_by))

    # Fetch all the results
    results = cursor.fetchall()

    # Print each resulting row
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()