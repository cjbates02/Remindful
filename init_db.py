import sqlite3

# Function to initialize the database
def initialize_database():
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("Remindful.db")
    cursor = connection.cursor()

    # Create the "Posts" table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Posts (
            post_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            first_name TEXT,
            last_name TEXT
        )
    ''')

    # Create the "Reply" table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Reply (
            reply_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            first_name TEXT,
            last_name TEXT,
            post_id INTEGER,
            FOREIGN KEY (post_id) REFERENCES Posts (post_id)
        )
    ''')

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()
    print("Remindful database initialized successfully.")
