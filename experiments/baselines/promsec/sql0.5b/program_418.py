import sqlite3

def fetch_patients_by_name():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_418_database.db')
    cursor = conn.cursor()
    
    # Prompt the user for input
    name = input("Enter a patient's name: ")
    
    # Construct the SQL query to fetch records where the name matches the input
    query = f"SELECT * FROM patients WHERE name = '{name}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all records from the query
    records = cursor.fetchall()
    
    # Print the results
    if records:
        print("Records found:")
        for record in records:
            print(record)
    else:
        print("No records found.")

# Call the function to fetch patients by name
fetch_patients_by_name()