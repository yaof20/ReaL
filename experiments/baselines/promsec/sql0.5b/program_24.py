import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_24_database.db')
    cursor = conn.cursor()

    # Prompt the user for input
    min_age = int(input("Enter the minimum age: "))
    max_age = int(input("Enter the maximum age: "))
    target_city = input("Enter the target city: ")
    include_younger = input("Include customers younger than the minimum age? (yes/no): ")

    # Construct the SQL query based on the inputs
    if include_younger == 'yes':
        query = f"SELECT * FROM customers WHERE age >= {min_age} AND age <= {max_age} AND city = '{target_city}'"
    else:
        query = f"SELECT * FROM customers WHERE age >= {min_age} AND age <= {max_age}"

    # Execute the query and fetch the results
    cursor.execute(query)
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()