import sqlite3

def get_sales_records():
    # Connect to the database
    conn = sqlite3.connect('program_126_database.db')
    cursor = conn.cursor()
    
    # Get user inputs
    upper_date = input("Enter the upper date bound (YYYY-MM-DD): ")
    quantity_increase = int(input("Enter the quantity increase value: "))
    category = input("Enter the category: ")
    
    # Calculate the date range
    from_date = (datetime.strptime(upper_date, '%Y-%m-%d') - timedelta(days=quantity_increase)).strftime('%Y-%m-%d')
    
    # Construct the SQL query
    query = f"""
    SELECT id, item, category, quantity, date
    FROM sales
    WHERE category = ? AND date BETWEEN ? AND ?
    """
    
    # Execute the query
    cursor.execute(query, (category, from_date, upper_date))
    
    # Fetch all records
    records = cursor.fetchall()
    
    # Print the results
    for record in records:
        print(record)
    
    # Close the connection
    conn.close()

# Call the function
get_sales_records()