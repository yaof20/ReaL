import sqlite3

def get_tickets_by_event(event_name, start_date, end_date, location):
    # Connect to the database
    conn = sqlite3.connect('program_277_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query based on the inputs
    query = f"SELECT * FROM tickets WHERE event_name = ? AND date BETWEEN ? AND ? AND location = ?"
    
    # Execute the query
    cursor.execute(query, (event_name, start_date, end_date, location))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    print(results)
    
    # Close the database connection
    conn.close()

# Example usage
get_tickets_by_event('Festival A', '2023-12-25', '2023-12-31', 'Denver')
get_tickets_by_event('Theatre Z', '2023-12-01', '2023-12-31', 'Philadelphia')