import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_217_database.db')
cursor = conn.cursor()

# Prompt user for inputs
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")
min_amount = float(input("Enter minimum amount due: "))
payment_status = input("Enter payment status: ")

# Build the SQL query
query = """
SELECT * FROM billing
WHERE billing_date BETWEEN ? AND ?
AND amount_due >= ?
AND status = ?
"""

# Execute the query
cursor.execute(query, (start_date, end_date, min_amount, payment_status))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()