import sqlite3

# Connect to the database
conn = sqlite3.connect('program_78_database.db')
cursor = conn.cursor()

# Get user inputs
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")
bulk_discount = float(input("Enter bulk discount percentage: "))
order_status = input("Enter order status: ")
price_threshold = float(input("Enter price threshold: "))

# Calculate the effective price threshold after applying the discount
effective_threshold = price_threshold * (1 - bulk_discount / 100)

# Construct the SQL query
query = f"""
SELECT * FROM orders
WHERE order_date BETWEEN ? AND ?
AND status = ?
AND total_price > ?
"""

# Execute the query
cursor.execute(query, (start_date, end_date, order_status, effective_threshold))

# Fetch and print the results
results = cursor.fetchall()
print(results)

# Close the connection
conn.close()