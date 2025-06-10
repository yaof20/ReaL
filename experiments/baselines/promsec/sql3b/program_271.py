import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_271_database.db')
cursor = conn.cursor()

# Get user inputs
min_age = input("Enter minimum age: ")
max_age = input("Enter maximum age: ")
ailment_filter = input("Enter ailment filter (or 'ANY' for no filter): ")
doctor_id_filter = input("Enter doctor ID filter (or 'ANY' for no filter): ")

# Construct the SQL query based on user inputs
query = "SELECT patient_id, first_name, last_name, age, ailment, doctor_id FROM patients"

if ailment_filter != 'ANY':
    query += f" WHERE ailment = '{ailment_filter}'"

if doctor_id_filter != 'ANY':
    if ailment_filter != 'ANY':
        query += " AND "
    query += f"doctor_id = {doctor_id_filter}"

if min_age != '':
    if ailment_filter != 'ANY' or doctor_id_filter != 'ANY':
        query += " AND "
    query += f"age >= {min_age}"

if max_age != '':
    if ailment_filter != 'ANY' or doctor_id_filter != 'ANY' or min_age != '':
        query += " AND "
    query += f"age <= {max_age}"

# Execute the query
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()