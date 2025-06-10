import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_197_database.db')
cursor = conn.cursor()

# Prompt user for start and end dates
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# Construct SQL query
query = "SELECT * FROM sales_data WHERE sale_date BETWEEN ? AND ?"

# Execute the query
cursor.execute(query, (start_date, end_date))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()