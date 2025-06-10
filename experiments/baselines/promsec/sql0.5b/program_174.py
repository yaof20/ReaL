import sqlite3

def get_studies_by_researcher(researcher_name):
    # Connect to the database
    conn = sqlite3.connect('program_174_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT study_id, researcher, research_subject, findings FROM studies WHERE researcher = ?"
    
    # Execute the query with the input researcher name
    cursor.execute(query, (researcher_name,))
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for study in results:
        print(f"({study[0]}, '{study[1]}', '{study[2]}', '{study[3]}')")
    
    # Close the connection
    conn.close()

# Example usage
researcher_name = input("Enter the researcher's name: ")
get_studies_by_researcher(researcher_name)