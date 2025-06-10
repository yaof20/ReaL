import sqlite3

def get_census_data(min_income, age, employment_status, adjustment_factor):
    # Connect to the database
    conn = sqlite3.connect('program_356_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = """
    SELECT citizen_id, full_name, age, city, income, employment_status
    FROM census_data
    WHERE income >= ? AND age = ? AND employment_status = ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (min_income, age, employment_status))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Example usage
min_income = float(input("Enter the minimum income threshold: "))
age = int(input("Enter the age: "))
employment_status = input("Enter the employment status: ")
adjustment_factor = float(input("Enter the adjustment factor: "))

get_census_data(min_income, age, employment_status, adjustment_factor)