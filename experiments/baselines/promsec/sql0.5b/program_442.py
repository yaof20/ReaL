import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_442_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    name = input("Enter player's name: ")
    team = input("Enter team name: ")
    points = int(input("Enter number of points to filter by: "))
    column = input("Enter column to display: ")
    order_direction = input("Enter order direction (ASC or DESC): ")

    # Construct the SQL query
    query = f"SELECT {column} FROM players WHERE name = ? AND team = ? AND points > ? ORDER BY {column} {order_direction}"

    # Execute the query
    cursor.execute(query, (name, team, points))

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()