import sqlite3

# Connect to the database
conn = sqlite3.connect('program_154_database.db')
cursor = conn.cursor()

# Prompt the user for input
location = input("Enter the location: ")

# Construct the SQL query
query = f"SELECT listing_id, title, description, price, location FROM listings WHERE location = '{location}'"

# Execute the query
cursor.execute(query)

# Fetch all matching records
records = cursor.fetchall()

# Print the results
for record in records:
    print(record)

# Close the database connection
conn.close()