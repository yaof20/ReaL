import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_271_database.db')
    cursor = conn.cursor()

    # Define the SQL query based on user inputs
    query = """
    SELECT patient_id, first_name, last_name, age, ailment, doctor_id
    FROM patients
    WHERE age BETWEEN ? AND ?
    AND (ailment = ? OR doctor_id = ?)
    """

    # Get user inputs
    min_age = int(input("Enter the minimum age: "))
    max_age = int(input("Enter the maximum age: "))
    ailment = input("Enter the ailment (ANY to exclude): ")
    doctor_id = input("Enter the doctor ID (ANY to exclude): ")

    # Construct the SQL query
    if ailment == 'ANY':
        query += " AND ailment IS NULL"
    if doctor_id == 'ANY':
        query += " AND doctor_id IS NULL"

    # Execute the query
    cursor.execute(query, (min_age, max_age, ailment, doctor_id))

    # Fetch all the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()