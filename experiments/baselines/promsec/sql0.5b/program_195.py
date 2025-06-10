import sqlite3

def get_posts_by_author(author_name, start_date, end_date, keyword):
    # Connect to the database
    conn = sqlite3.connect('program_195_database.db')
    cursor = conn.cursor()
    
    # Construct the SQL query
    query = """
    SELECT post_id, title, content, author, publish_date
    FROM posts
    WHERE author = ?
    AND publish_date BETWEEN ?
    AND ?
    AND (title LIKE ? OR content LIKE ?)
    """
    
    # Execute the query with the provided inputs
    cursor.execute(query, (author_name, start_date, end_date, keyword, keyword))
    
    # Fetch all the results
    posts = cursor.fetchall()
    
    # Print the results
    for post in posts:
        print(f"Post ID: {post[0]}, Title: {post[1]}, Content: {post[2]}, Author: {post[3]}, Publish Date: {post[4]}")
    
    # Close the database connection
    conn.close()

# Example usage
get_posts_by_author('Charlie', '2023-04-01', '2023-08-01', 'Insights')
get_posts_by_author('Alice', '2023-01-01', '2023-05-31', 'first')