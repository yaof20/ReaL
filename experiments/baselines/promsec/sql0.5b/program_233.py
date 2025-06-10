import sqlite3

def get_events(location, earliest_date, latest_date):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_233_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM events WHERE location = ? AND date BETWEEN ? AND ?"
    
    # Execute the query with the provided inputs
    cursor.execute(query, (location, earliest_date, latest_date))
    
    # Fetch all the rows from the query
    events = cursor.fetchall()
    
    # Close the database connection
    conn.close()
    
    return events

# Example usage
location = input("Enter the event location: ")
earliest_date = input("Enter the earliest date (YYYY-MM-DD): ")
latest_date = input("Enter the latest date (YYYY-MM-DD): ")

events = get_events(location, earliest_date, latest_date)
print(events)