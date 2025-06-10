import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_298_database.db')
    cursor = conn.cursor()

    # Prompt user for inputs
    start_year = int(input("Enter the starting publication year: "))
    end_year = int(input("Enter the ending publication year: "))
    genre = input("Enter the genre: ")
    author_name = input("Enter the author's name (partial or full): ")

    # Build the SQL query
    query = """
    SELECT id, title, author, year, genre
    FROM books
    WHERE year BETWEEN ? AND ?
    AND genre = ?
    AND author LIKE ?
    """
    cursor.execute(query, (start_year, end_year, genre, f'%{author_name}%'))

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()