import sqlite3

def query_players(min_avg_score, max_avg_score, desired_position, team_name):
    # Connect to the database
    conn = sqlite3.connect('program_341_database.db')
    cursor = conn.cursor()
    
    # Define the SQL query
    query = """
    SELECT id, name, team, avg_score, position
    FROM player_stats
    WHERE avg_score BETWEEN ? AND ?
    AND position = ?
    AND team != ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (min_avg_score, max_avg_score, desired_position, team_name))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the database connection
    conn.close()

# Example usage
query_players(17, 23, 'Forward', 'Lions')
query_players(15, 19, 'Guard', 'Lions')