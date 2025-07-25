import sqlite3

def setup_resibot_database():
    """Creates the database file and the conversation state table."""
    try:
        # This will create the file 'receipts.db' if it doesn't exist
        connection = sqlite3.connect('receipts.db')
        cursor = connection.cursor()

        # SQL query to create the table if it's not already there
        create_table_query = """
        CREATE TABLE IF NOT EXISTS telegram_receipts (
            chatId TEXT PRIMARY KEY,
            state TEXT NOT NULL,
            receipt_json TEXT
        );
        """

        cursor.execute(create_table_query)
        connection.commit()
        print("Database 'receipts.db' is ready.")

    except sqlite3.Error as error:
        print(f"Error while setting up SQLite database: {error}")

    finally:
        if connection:
            connection.close()
            print("The SQLite connection is closed.")

def get_conn():
    conn = sqlite3.connect('receipts.db') # Assumes the DB file is in the same folder
    conn.row_factory = sqlite3.Row
    return conn 