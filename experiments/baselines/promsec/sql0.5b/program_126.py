import sqlite3

def get_sales_data():
    # Connect to the database
    conn = sqlite3.connect('program_126_database.db')
    cursor = conn.cursor()
    
    # Get user inputs
    upper_date = input("Enter the upper date bound in the format 'YYYY-MM-DD': ")
    quantity_increase = int(input("Enter the quantity increase value: "))
    category = input("Enter the category: ")
    
    # Calculate the date range
    start_date = upper_date
    end_date = start_date + timedelta(days=quantity_increase)
    
    # Construct the SQL query
    query = f"SELECT * FROM sales WHERE category = '{category}' AND date BETWEEN '{start_date}' AND '{end_date}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for row in results:
        print(row)
    
    # Close the connection
    conn.close()

# Call the function to get sales data
get_sales_data()