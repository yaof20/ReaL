import sqlite3

def search_users(min_friends, max_friends, age_preference, keyword):
    # Connect to the database
    conn = sqlite3.connect('program_215_database.db')
    cursor = conn.cursor()
    
    # Adjust the friends_count range by subtracting 10 from the minimum and adding 10 to the maximum
    min_friends -= 10
    max_friends += 10
    
    # Construct the SQL query
    query = f"SELECT user_id, username, bio, age, friends_count FROM users WHERE friends_count BETWEEN {min_friends} AND {max_friends} AND age >= {age_preference} AND bio LIKE '%{keyword}%'"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all the results
    results = cursor.fetchall()
    
    # Print the results
    for user in results:
        print(f"({user[0]}, '{user[1]}', '{user[2]}', {user[3]}, {user[4]})")
    
    # Close the connection
    conn.close()

# Example usage
search_users(40, 100, 29, 'Loves')
search_users(0, 80, 25, 'Adventurous')