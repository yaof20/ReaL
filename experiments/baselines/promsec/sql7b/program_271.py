import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_271_database.db')
cursor = conn.cursor()

# Get user inputs
min_age = int(input("Enter minimum age: "))
max_age = int(input("Enter maximum age: "))
ailment_filter = input("Enter ailment (or 'ANY' for no filter): ")
doctor_id_filter = input("Enter doctor ID (or 'ANY' for no filter): ")

# Construct the SQL query
query = "SELECT * FROM patients WHERE age BETWEEN ? AND ?"
params = [min_age, max_age]

# Add ailment filter if not 'ANY'
if ailment_filter != 'ANY':
    query += " AND ailment = ?"
    params.append(ailment_filter)

# Add doctor ID filter if not 'ANY'
if doctor_id_filter != 'ANY':
    query += " AND doctor_id = ?"
    params.append(doctor_id_filter)

# Execute the query
cursor.execute(query, params)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the connection
conn.close()