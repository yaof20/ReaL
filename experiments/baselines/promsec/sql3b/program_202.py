import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('program_202_database.db')
cursor = conn.cursor()

# Prompt the user for inputs
phone_number = input("Enter a phone number: ")
min_amount_due = float(input("Enter a minimum amount due: "))

# Construct the SQL query
query = f"SELECT customer_id, name, phone, amount_due FROM customer_bills WHERE phone = ? AND amount_due > ?"

# Execute the query with the user inputs
cursor.execute(query, (phone_number, min_amount_due))

# Fetch all the results
results = cursor.fetchall()

# Print the results
for result in results:
    print(result)

# Close the database connection
conn.close()