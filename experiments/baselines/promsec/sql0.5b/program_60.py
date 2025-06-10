import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_60_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
min_price = float(input("Enter the minimum price: "))
max_price = float(input("Enter the maximum price: "))
genre = input("Enter the genre: ")

# Adjust the minimum and maximum prices
adjusted_min_price = min_price * 1.10
adjusted_max_price = max_price * 1.10

# Construct the SQL query
query = f"SELECT title, author, price, genre FROM books WHERE price BETWEEN {adjusted_min_price} AND {adjusted_max_price} AND genre = '{genre}'"

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(f"Title: {row[0]}, Author: {row[1]}, Price: {row[2]}, Genre: {row[3]}")

# Close the database connection
conn.close()