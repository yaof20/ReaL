import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_301_database.db')
cursor = conn.cursor()

# Prompt the user to input a campaign name
campaign_name = input("Enter the campaign name: ")

# Construct the SQL query to search for the campaign name
query = f"SELECT * FROM marketing_campaigns WHERE campaign_name = '{campaign_name}'"

# Execute the query
cursor.execute(query)

# Fetch all the records
results = cursor.fetchall()

# Check if any records were found
if results:
    # Print each record
    for row in results:
        print(row)
else:
    # Print a message if no matching campaign was found
    print("No matching campaign found.")

# Close the database connection
conn.close()