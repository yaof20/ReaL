import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_75_database.db')
cursor = conn.cursor()

# Get user inputs
min_weight = float(input())
max_weight = float(input())
min_rating = float(input())
category = input()

# Adjust the weight and rating based on user inputs
adjusted_min_weight = min_weight * 0.95
adjusted_max_weight = max_weight * 1.05
adjusted_min_rating = min_rating + 0.3

# Build the SQL query
query = f"SELECT * FROM items WHERE weight BETWEEN {adjusted_min_weight} AND {adjusted_max_weight} AND rating >= {adjusted_min_rating} AND category = '{category}'"

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()