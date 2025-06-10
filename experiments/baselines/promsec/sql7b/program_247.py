import sqlite3

# Connect to the database
conn = sqlite3.connect('program_247_database.db')
cursor = conn.cursor()

# Get user inputs
start_year = int(input("Enter the start year of publication: "))
end_year = int(input("Enter the end year of publication: "))
min_citations = int(input("Enter the minimum number of citations: "))
field = input("Enter the research field: ")

# Construct the SQL query
query = f"SELECT * FROM papers WHERE year BETWEEN {start_year} AND {end_year} AND field = ? AND citations >= {min_citations}"

# Execute the query
cursor.execute(query, (field,))

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the database connection
conn.close()