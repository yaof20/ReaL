import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_198_database.db')
cursor = conn.cursor()

# Prompt the user for input
min_rating = int(input("Enter the minimum acceptable rating: "))
max_rating = int(input("Enter the maximum acceptable rating: "))
customer_name = input("Enter the specific customer name: ")

# Construct the SQL query based on user inputs
query = f"""
SELECT * FROM feedback
WHERE (rating BETWEEN {min_rating} AND {max_rating})
OR (customer_name = '{customer_name}')
"""

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()