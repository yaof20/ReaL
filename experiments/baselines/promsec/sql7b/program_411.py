import sqlite3

# Function to get user inputs
def get_user_inputs():
    campaign_id = int(input("Enter campaign ID: "))
    metric = input("Enter metric (clicks, impressions, conversion_rate): ")
    min_value = float(input("Enter minimum value for the metric: "))
    return campaign_id, metric, min_value

# Function to construct and execute SQL query
def fetch_data(campaign_id, metric, min_value):
    # Connect to the database
    conn = sqlite3.connect('program_411_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT name, {metric} FROM campaign_analytics WHERE campaign_id = ? AND {metric} >= ?"
    
    # Execute the query
    cursor.execute(query, (campaign_id, min_value))
    
    # Fetch and print the results
    results = cursor.fetchall()
    for result in results:
        print(result)
    
    # Close the connection
    conn.close()

# Main function to handle the workflow
def main():
    campaign_id, metric, min_value = get_user_inputs()
    fetch_data(campaign_id, metric, min_value)

# Run the main function
if __name__ == "__main__":
    main()