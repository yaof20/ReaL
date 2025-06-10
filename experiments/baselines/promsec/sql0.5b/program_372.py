import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_372_database.db')
    cursor = conn.cursor()

    # Define the SQL query based on the user inputs
    query = """
    SELECT *
    FROM patients
    WHERE doctor = ?
    AND age BETWEEN ? AND ?
    AND (treatment = ? OR diagnosis = ?)
    ORDER BY ?
    """

    # Get user inputs
    doctor_name = input("Enter the doctor's name: ")
    min_age = int(input("Enter the minimum age range (e.g., 30): "))
    max_age = int(input("Enter the maximum age range (e.g., 50): "))
    treatment = input("Enter the search field (e.g., treatment, diagnosis, or patient_id): ")
    search_value = input("Enter the search value: ")
    column_to_order = input("Enter the column to order the results by (e.g., patient_id, name, or age): ")
    order_direction = input("Enter the order direction (ASC or DESC): ")

    # Construct the SQL query
    query = query.format(doctor_name, min_age, max_age, treatment, search_value, column_to_order, order_direction)

    # Execute the SQL query
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