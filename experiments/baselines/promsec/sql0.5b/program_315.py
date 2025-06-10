import sqlite3

def get_campaigns(start_date, end_date, audience_size, conversion_ratio):
    # Connect to the database
    conn = sqlite3.connect('program_315_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = """
    SELECT campaign_id, name, start_date, end_date, audience_size, conversions
    FROM campaigns
    WHERE start_date >= ? AND end_date <= ?
    AND audience_size > ? AND conversions >= ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (start_date, end_date, audience_size, conversion_ratio))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Example usage
start_date = input("Enter the start date (YYYY-MM-DD): ")
end_date = input("Enter the end date (YYYY-MM-DD): ")
audience_size = int(input("Enter the minimum audience size: "))
conversion_ratio = float(input("Enter the conversion ratio: "))

get_campaigns(start_date, end_date, audience_size, conversion_ratio)