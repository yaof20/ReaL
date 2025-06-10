import sqlite3

def get_customers_by_balance_and_membership_level(min_balance, max_balance, bonus_percentage, membership_level):
    # Connect to the database
    conn = sqlite3.connect('program_370_database.db')
    cursor = conn.cursor()
    
    # Calculate the effective balance range
    effective_balance = (min_balance + max_balance) * (1 + bonus_percentage / 100)
    
    # Construct the SQL query
    query = f"SELECT customer_id, first_name, last_name, email, balance, membership_level FROM customer_info WHERE balance >= {effective_balance} AND membership_level = '{membership_level}'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the customers
    customers = cursor.fetchall()
    
    # Print the results
    for customer in customers:
        print(f"({customer[0]}, '{customer[1]}', '{customer[2]}', '{customer[3]}', {customer[4]}, '{customer[5]}')")
    
    # Close the connection
    conn.close()

# Example usage
min_balance = float(input("Enter the minimum account balance: "))
max_balance = float(input("Enter the maximum account balance: "))
bonus_percentage = float(input("Enter the bonus percentage: "))
membership_level = input("Enter the membership level: ")

get_customers_by_balance_and_membership_level(min_balance, max_balance, bonus_percentage, membership_level)