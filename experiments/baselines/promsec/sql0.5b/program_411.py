import sqlite3

def get_campaign_data(campaign_id, metric, min_value):
    # Connect to the database
    conn = sqlite3.connect('program_411_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT name, {metric} FROM campaign_analytics WHERE campaign_id = ? AND {metric} >= ?"
    
    # Execute the query with the provided inputs
    cursor.execute(query, (campaign_id, min_value))
    
    # Fetch the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(f"'{row[0]}' - {row[1]}")
    
    # Close the database connection
    conn.close()

# Example usage
get_campaign_data(4, 'impressions', 1500)
get_campaign_data(5, 'conversion_rate', 0.1)