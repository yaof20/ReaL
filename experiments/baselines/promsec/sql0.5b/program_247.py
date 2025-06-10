import sqlite3

# Connect to the database
conn = sqlite3.connect('program_247_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
start_year = input("Enter the start year of publication: ")
end_year = input("Enter the end year of publication: ")
min_citations = input("Enter the minimum number of citations: ")
research_field = input("Enter the research field: ")

# Construct the SQL query
query = f"""
SELECT id, title, author, year, field, citations
FROM papers
WHERE year BETWEEN {start_year} AND {end_year}
AND field = '{research_field}'
AND citations >= {min_citations}
"""

# Execute the query
cursor.execute(query)

# Fetch all the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the database connection
conn.close()