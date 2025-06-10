import sqlite3

def query_census_data(city, min_age, min_income):
    # Connect to the database
    conn = sqlite3.connect('program_391_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT * FROM census_data WHERE city = ? AND age >= ? AND income >= ?"
    
    # Execute the query
    cursor.execute(query, (city, min_age, min_income))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Example usage
city_input = input("Enter the city name: ")
min_age_input = input("Enter the minimum age: ")
min_income_input = input("Enter the minimum income: ")

query_census_data(city_input, min_age_input, min_income_input)