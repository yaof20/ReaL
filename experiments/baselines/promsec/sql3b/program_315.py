import sqlite3

def get_campaigns():
    # Connect to the database
    conn = sqlite3.connect('program_315_database.db')
    cursor = conn.cursor()
    
    # Prompt user for inputs
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    min_audience_size = int(input("Enter minimum audience size: "))
    conversion_ratio = float(input("Enter conversion ratio: "))
    
    # Construct the SQL query
    query = """
    SELECT campaign_id, name, start_date, end_date, audience_size, conversions
    FROM campaigns
    WHERE (start_date >= ? AND end_date <= ?)
    OR (audience_size > ?)
    OR (conversions >= ? * audience_size)
    """
    cursor.execute(query, (start_date, end_date, min_audience_size, conversion_ratio))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    for result in results:
        print(result)
    
    # Close the connection
    conn.close()

# Call the function
get_campaigns()