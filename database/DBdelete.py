import sqlite3

def execute_query(query: str, params: tuple = ()):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print("Error executing query:", e)
    finally:
        conn.close()


def clear_mention_table(username: str):
    query = "DELETE FROM mention_table WHERE username = ?"
    execute_query(query, (username,))


def clear_nuke_table():
    query = "DELETE FROM nuke_table"
    execute_query(query)


def clear_database():
    queries = [
        "DELETE FROM users",
        "DELETE FROM channels",
        "DELETE FROM words",
        "DELETE FROM userwords",
        "DELETE FROM channelwords"
    ]
    for query in queries:
        execute_query(query)
    print("Tables deleted successfully.")
