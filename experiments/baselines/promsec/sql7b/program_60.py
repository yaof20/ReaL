import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_60_database.db')
cursor = conn.cursor()

# Prompt user for inputs
min_price = float(input("Enter minimum price: "))
max_price = float(input("Enter maximum price: "))
genre = input("Enter genre: ")

# Adjust the price range
adjusted_min_price = min_price * 0.9
adjusted_max_price = max_price * 1.1

# Build the SQL query
query = "SELECT title, author, price, genre FROM books WHERE price BETWEEN ? AND ? AND genre = ?"

# Execute the query
cursor.execute(query, (adjusted_min_price, adjusted_max_price, genre))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(f"Title: {row[0]}, Author: {row[1]}, Price: {row[2]}, Genre: {row[3]}")

# Close the connection
conn.close()