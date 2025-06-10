import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_75_database.db')
cursor = conn.cursor()

# Define the minimum and maximum weight, minimum rating, and category
min_weight = float(input("Enter the minimum weight: "))
max_weight = float(input("Enter the maximum weight: "))
min_rating = float(input("Enter the minimum rating: "))
category = input("Enter the category: ")

# Calculate the range for weight and rating
weight_range = (min_weight * 0.95, max_weight * 1.05)
rating_range = (min_rating + 0.3, min_rating + 0.3)

# Construct the SQL query
query = f"SELECT * FROM items WHERE weight BETWEEN {weight_range[0]} AND {weight_range[1]} AND rating >= {rating_range[0]} AND category = '{category}'"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for item in results:
    print(item)

# Close the database connection
conn.close()