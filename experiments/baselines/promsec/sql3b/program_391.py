import sqlite3

def query_census_data():
    # Connect to the database
    conn = sqlite3.connect('program_391_database.db')
    cursor = conn.cursor()
    
    # Get user inputs
    city = input("Enter the city: ")
    min_age = int(input("Enter the minimum age: "))
    min_income = float(input("Enter the minimum income: "))
    
    # Build the SQL query
    query = """
    SELECT citizen_id, name, age, city, income
    FROM census_data
    WHERE city = ? AND (age >= ? OR income >= ?)
    """
    
    # Execute the query
    cursor.execute(query, (city, min_age, min_income))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    print(results)
    
    # Close the connection
    conn.close()

# Call the function
query_census_data()