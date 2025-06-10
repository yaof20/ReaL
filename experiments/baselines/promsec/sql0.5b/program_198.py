import sqlite3

def get_feedback(min_rating, max_rating, customer_name):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_198_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = """
    SELECT id, customer_name, rating, feedback
    FROM feedback
    WHERE rating BETWEEN ? AND ?
    OR customer_name = ?
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (min_rating, max_rating, customer_name))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the database connection
    conn.close()

# Example usage
min_rating = int(input("Enter the minimum acceptable rating: "))
max_rating = int(input("Enter the maximum acceptable rating: "))
customer_name = input("Enter the customer name: ")

get_feedback(min_rating, max_rating, customer_name)