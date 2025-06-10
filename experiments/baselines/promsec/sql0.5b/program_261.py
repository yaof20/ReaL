import sqlite3

def query_tickets(event_location, min_price, max_price, discount_percentage):
    # Connect to the database
    conn = sqlite3.connect('program_261_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = """
    SELECT event_id, event_name, location, ticket_price
    FROM tickets
    WHERE location = ?
    AND ticket_price BETWEEN ? AND ?
    AND ticket_price * (1 - discount_percentage / 100) > ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (event_location, min_price, max_price, min_price * (1 - discount_percentage / 100)))
    
    # Fetch all the matching events
    events = cursor.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Print the matching events
    for event in events:
        print(event)

# Example usage
query_tickets('San Francisco', 50, 300, 0.10)
query_tickets('Las Vegas', 50, 210, 0.05)