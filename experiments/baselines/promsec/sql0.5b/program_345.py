import sqlite3

def get_papers_by_year_and_category(year, category):
    # Connect to the database
    conn = sqlite3.connect('program_345_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"SELECT paper_id, title, author, year_published, category, abstract FROM papers WHERE year_published = ? AND category = ?"
    
    # Execute the query with the provided inputs
    cursor.execute(query, (year, category))
    
    # Fetch all the results
    papers = cursor.fetchall()
    
    # Print the results
    for paper in papers:
        print(f"Paper ID: {paper[0]}, Title: {paper[1]}, Author: {paper[2]}, Year Published: {paper[3]}, Category: {paper[4]}, Abstract: {paper[5]}")
    
    # Close the database connection
    conn.close()

# Example usage
year = input("Enter the publication year: ")
category = input("Enter the research category: ")
get_papers_by_year_and_category(year, category)