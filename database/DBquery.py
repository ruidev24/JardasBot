import sqlite3
import random


# Utility function for database connection
def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    try:
        with sqlite3.connect("wordstats.db") as conn:
            c = conn.cursor()
            c.execute(query, params or ())
            if fetch_one:
                return c.fetchone()
            if fetch_all:
                return c.fetchall()
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    return None


#################################################
def query_strangers_vocabulary():
    result = execute_query(
        "SELECT * FROM vocabulary_table", fetch_all=True
    )
    if result:
        return random.choice(result)[0]
    return None


#################################################
def query_mention_count(username):
    result = execute_query(
        "SELECT * FROM mention_table WHERE username = ?", (username,), fetch_one=True
    )
    if result:
        mention_cnt = result[1]
        print(f"mention_cnt {mention_cnt}")
        return mention_cnt
    return 0


#################################################
def query_nuke_count():
    nuke_cnt = execute_query(
        "SELECT SUM(nuke_count) FROM nuke_table", fetch_one=True
    )
    defuse_cnt = execute_query(
        "SELECT SUM(defuse_count) FROM nuke_table", fetch_one=True
    )

    nuke_total = nuke_cnt[0] if nuke_cnt and nuke_cnt[0] else 0
    defuse_total = defuse_cnt[0] if defuse_cnt and defuse_cnt[0] else 0
    return nuke_total - defuse_total


#################################################
def query_fortune_last_date(username):
    result = execute_query(
        "SELECT * FROM fortune_table WHERE user = ?", (username,), fetch_one=True
    )
    return result if result else None


#################################################
def query_nuke_last_date():
    result = execute_query(
        "SELECT * FROM nuke_table ORDER BY date DESC LIMIT 1", fetch_one=True
    )
    if result:
        return result[3]  # Assuming the date is in the 4th column
    return None


#################################################
def query_mention_last_date(username):
    result = execute_query(
        "SELECT * FROM mention_table WHERE username = ?", (username,), fetch_one=True
    )
    if result:
        return result[2]  # Assuming the date is in the 3rd column
    return None


#################################################
def query_least_favourable():
    least_favourable = execute_query(
        "SELECT * FROM favour_table ORDER BY favour ASC LIMIT 1", fetch_one=True
    )
    if least_favourable:
        username = least_favourable[0]
        user_item = execute_query(
            "SELECT * FROM users WHERE username = ?", (username,), fetch_one=True
        )
        if user_item:
            return user_item[0]  # Assuming server nickname is in the 1st column
    return None
