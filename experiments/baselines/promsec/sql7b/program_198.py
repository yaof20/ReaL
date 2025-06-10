import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_198_database.db')
cursor = conn.cursor()

# Prompt user for inputs
min_rating = int(input("Enter the minimum acceptable rating: "))
max_rating = int(input("Enter the maximum acceptable rating: "))
customer_name = input("Enter the specific customer name: ")

# Construct the SQL query based on user inputs
query = """
SELECT * FROM feedback
WHERE (rating BETWEEN ? AND ?) OR customer_name = ?
"""

# Execute the query
cursor.execute(query, (min_rating, max_rating, customer_name))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()