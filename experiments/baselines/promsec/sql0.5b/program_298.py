import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_298_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    start_year = int(input("Enter the starting publication year: "))
    end_year = int(input("Enter the ending publication year: "))
    genre = input("Enter the genre: ")
    author_name = input("Enter the author's name (partial or full): ")

    # Construct the SQL query
    query = f"""
    SELECT id, title, author, year, genre
    FROM books
    WHERE year BETWEEN {start_year} AND {end_year}
    AND genre = '{genre}'
    AND author LIKE '%{author_name}%'
    """

    # Execute the query
    cursor.execute(query)

    # Fetch all the matching records
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()