import sqlite3

def search_users(min_friends, max_friends, age_preference, keyword):
    # Connect to the database
    conn = sqlite3.connect('program_215_database.db')
    cursor = conn.cursor()
    
    # Adjust the friends_count range
    min_friends -= 10
    max_friends += 10
    
    # Construct the SQL query
    query = """
    SELECT user_id, username, bio, age, friends_count
    FROM users
    WHERE friends_count BETWEEN ? AND ?
    AND age = ?
    AND bio LIKE ?
    """
    
    # Execute the query
    cursor.execute(query, (min_friends, max_friends, age_preference, f'%{keyword}%'))
    
    # Fetch all results
    results = cursor.fetchall()
    
    # Print the results
    for result in results:
        print(result)
    
    # Close the connection
    conn.close()

# Example usage
min_friends = int(input("Enter the minimum number of friends: "))
max_friends = int(input("Enter the maximum number of friends: "))
age_preference = int(input("Enter the age preference: "))
keyword = input("Enter the keyword to search within the bio: ")

search_users(min_friends, max_friends, age_preference, keyword)