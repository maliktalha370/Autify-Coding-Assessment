import sqlite3

def setup_database():
    conn = sqlite3.connect('feedback.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS feedback
                 (id INTEGER PRIMARY KEY, helpful TEXT, comments TEXT)''')

    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()

def save_feedback(feedback_data):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('feedback.db')
        c = conn.cursor()

        # Insert a row of feedback
        c.execute("INSERT INTO feedback (helpful, comments) VALUES (?, ?)",
                  (feedback_data['helpful'], feedback_data['comments']))

        # Save (commit) the changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")
        return False

    finally:
        # Close the connection to the database
        conn.close()

    return True

if __name__=='__main__':
    setup_database()