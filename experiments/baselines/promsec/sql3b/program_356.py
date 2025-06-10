import sqlite3

def fetch_census_data(min_income, age, employment_status, adjustment_factor):
    # Connect to the database
    conn = sqlite3.connect('program_356_database.db')
    cursor = conn.cursor()
    
    # Adjust the minimum income
    adjusted_min_income = min_income + adjustment_factor
    
    # Construct the SQL query
    query = """
    SELECT citizen_id, full_name, age, city, income, employment_status
    FROM census_data
    WHERE income >= ? OR age = ? OR employment_status = ?
    """
    
    # Execute the query
    cursor.execute(query, (adjusted_min_income, age, employment_status))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for result in results:
        print(result)
    
    # Close the connection
    conn.close()

# Example usage
if __name__ == "__main__":
    # Get user inputs
    min_income = int(input("Enter the minimum income threshold: "))
    age = int(input("Enter the age: "))
    employment_status = input("Enter the employment status: ")
    adjustment_factor = int(input("Enter the adjustment factor: "))
    
    # Call the function with the user inputs
    fetch_census_data(min_income, age, employment_status, adjustment_factor)