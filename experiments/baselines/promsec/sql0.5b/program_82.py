import sqlite3

def get_user_email(username):
    # Connect to the SQLite database
    conn = sqlite3.connect('program_82_database.db')
    cursor = conn.cursor()
    
    # SQL query to find the email based on the provided username
    query = "SELECT email FROM users WHERE username = ?"
    
    # Execute the query with the provided username
    cursor.execute(query, (username,))
    
    # Fetch the result
    result = cursor.fetchone()
    
    # Close the database connection
    conn.close()
    
    # Print the result
    if result:
        print(result[0])
    else:
        print("User not found.")

# Example usage
get_user_email(input("Enter username: "))