import sqlite3

def get_tickets(min_price, max_price, event_date, event_name):
    # Connect to the database
    conn = sqlite3.connect('program_407_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = """
    SELECT ticket_id, event_name, date, price
    FROM tickets
    WHERE price BETWEEN ? AND ?
    AND date = ?
    AND event_name LIKE ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (min_price, max_price, event_date, event_name))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Example usage
get_tickets(30, 70, '2023-12-06', 'Show')
get_tickets(70, 120, '2023-12-10', 'Festival')