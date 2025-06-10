import sqlite3

def get_population_greater_than_threshold_and_state(abbreviation, threshold):
    # Connect to the database
    conn = sqlite3.connect('program_172_database.db')
    cursor = conn.cursor()
    
    # Define the SQL query
    query = f"SELECT * FROM population WHERE population > {threshold} AND state = '{abbreviation}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    print(results)
    
    # Close the database connection
    conn.close()

# Example usage
population_threshold = input("Enter the population threshold: ")
state_abbreviation = input("Enter the state abbreviation: ")

get_population_greater_than_threshold_and_state(state_abbreviation, population_threshold)