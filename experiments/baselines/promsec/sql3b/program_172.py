import sqlite3

def get_population_data(threshold, state):
    # Connect to the database
    conn = sqlite3.connect('program_172_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM population WHERE population > {threshold} AND state = '{state}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Close the database connection
    conn.close()
    
    return results

# Get user inputs
threshold = int(input("Enter the population threshold: "))
state = input("Enter the state abbreviation: ")

# Get the population data
results = get_population_data(threshold, state)

# Print the results
print(results)