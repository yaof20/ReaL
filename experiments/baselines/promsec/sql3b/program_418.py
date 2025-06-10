import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_418_database.db')
cursor = conn.cursor()

# Prompt the user to enter a patient's name
patient_name = input("Enter a patient's name: ")

# Construct the SQL query to retrieve records where the name matches the user's input
query = f"SELECT * FROM patients WHERE name = '{patient_name}'"

# Execute the query
cursor.execute(query)

# Fetch all records from the query result
records = cursor.fetchall()

# Check if any records were found
if records:
    # Print each record
    for record in records:
        print(record)
else:
    # Print a message if no records were found
    print("No records found.")

# Close the database connection
conn.close()