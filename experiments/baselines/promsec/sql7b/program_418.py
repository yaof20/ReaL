import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_418_database.db')
cursor = conn.cursor()

# Prompt the user to enter a patient's name
patient_name = input("Enter a patient's name: ")

# SQL query to fetch records where the name matches the user input
query = "SELECT * FROM patients WHERE name = ?"
cursor.execute(query, (patient_name,))

# Fetch all matching records
records = cursor.fetchall()

# Check if any records were found and print them
if records:
    for record in records:
        print(record)
else:
    print("No records found.")

# Close the database connection
conn.close()