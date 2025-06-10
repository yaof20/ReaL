import sqlite3

def get_items_from_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_75_database.db')
    cursor = conn.cursor()
    
    # Get user inputs
    min_weight = float(input("Enter the minimum weight: "))
    max_weight = float(input("Enter the maximum weight: "))
    min_rating = float(input("Enter the minimum rating: "))
    category = input("Enter the desired category: ")
    
    # Adjust the weight range
    adjusted_min_weight = min_weight * 0.95
    adjusted_max_weight = max_weight * 1.05
    
    # Adjust the minimum rating
    adjusted_min_rating = min_rating + 0.3
    
    # Construct the SQL query
    query = f"""
    SELECT * FROM items
    WHERE weight BETWEEN {adjusted_min_weight} AND {adjusted_max_weight}
    AND rating >= {adjusted_min_rating}
    AND category = '{category}'
    """
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    for item in results:
        print(item)
    
    # Close the database connection
    conn.close()

# Call the function
get_items_from_database()