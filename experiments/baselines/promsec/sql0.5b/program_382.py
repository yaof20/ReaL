import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_382_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    min_age = int(input("Enter the minimum age: "))
    country = input("Enter the country: ")
    keyword = input("Enter the keyword to search within the bio column: ")

    # Construct the SQL query
    query = f"SELECT * FROM users WHERE age >= {min_age} OR country = '{country}' OR bio LIKE '%{keyword}%'"

    # Execute the query
    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()