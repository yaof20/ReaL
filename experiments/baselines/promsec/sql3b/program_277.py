import sqlite3

def get_tickets(event_name, start_date, end_date, location):
    # Connect to the database
    conn = sqlite3.connect('program_277_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query based on user inputs
    query = "SELECT * FROM tickets WHERE 1=1"
    
    if event_name != 'all':
        query += f" AND event_name = '{event_name}'"
    
    if start_date:
        query += f" AND date >= '{start_date}'"
    
    if end_date:
        query += f" AND date <= '{end_date}'"
    
    if location:
        query += f" AND location = '{location}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    return results

# Get user inputs
event_name = input("Enter the event name (or 'all' to match any event): ")
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
location = input("Enter the location: ")

# Get and print the tickets
tickets = get_tickets(event_name, start_date, end_date, location)
print(tickets)