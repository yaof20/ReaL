import sqlite3

# Connect to the database
conn = sqlite3.connect('program_154_database.db')
cursor = conn.cursor()

# Prompt the user for the location
location = input("Enter the location: ")

# Construct the SQL query
query = f"SELECT listing_id, title, description, price, location FROM listings WHERE location = ?"

# Execute the query
cursor.execute(query, (location,))

# Fetch all the matching records
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()