import sqlite3

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('program_18_database.db')
    cursor = conn.cursor()

    # Prompt the user for inputs
    salary_multiplier = float(input("Enter the salary multiplier: "))
    bonus_amount = float(input("Enter the bonus amount: "))
    department_name = input("Enter the department name: ")

    # Calculate the minimum and maximum salary range
    min_salary = salary_multiplier * bonus_amount
    max_salary = min_salary + bonus_amount

    # Construct the SQL query
    query = f"SELECT id, name, department, salary FROM employees WHERE salary BETWEEN {min_salary} AND {max_salary} AND department = '{department_name}'"

    # Execute the query and print the results
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()