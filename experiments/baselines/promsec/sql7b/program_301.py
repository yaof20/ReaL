import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_301_database.db')
cursor = conn.cursor()

# Prompt the user to input a campaign name
campaign_name = input("Enter a campaign name: ")

# SQL query to retrieve records matching the campaign name
query = "SELECT * FROM marketing_campaigns WHERE campaign_name = ?"

# Execute the query
cursor.execute(query, (campaign_name,))

# Fetch all matching records
records = cursor.fetchall()

# Check if any records were found
if records:
    for record in records:
        print(record)
else:
    print("No matching campaign found.")

# Close the database connection
conn.close()