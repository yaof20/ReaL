import sqlite3

def get_reservations(room_type, check_in_date, check_out_date, max_price):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_353_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = f"""
    SELECT reservation_id, guest_name, room_type, check_in_date, check_out_date, price
    FROM reservations
    WHERE room_type = '{room_type}'
    AND check_in_date >= '{check_in_date}'
    AND check_out_date <= '{check_out_date}'
    AND price <= {max_price}
    """
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the results
    reservations = cursor.fetchall()
    
    # Print the results
    for reservation in reservations:
        print(reservation)
    
    # Close the connection
    conn.close()

# Example usage
room_type = input("Enter the room type (e.g., Single, Double, Suite): ")
check_in_date = input("Enter the check-in date (YYYY-MM-DD): ")
check_out_date = input("Enter the check-out date (YYYY-MM-DD): ")
max_price = float(input("Enter the maximum price (float): "))

get_reservations(room_type, check_in_date, check_out_date, max_price)