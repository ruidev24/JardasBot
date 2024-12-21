import datetime
from database.DBhelpers import db_execute_query, db_select_all, db_select_one

def clear_nuke_table():
    query = "DELETE FROM nuke_table"
    db_execute_query(query)


def update_nuke_count(username):
    today = datetime.date.today()
    is_repeat = db_select_one("SELECT 1 FROM nuke_table WHERE username = ?", (str(username),) )
    query = """INSERT INTO nuke_table (username, nuke_count, defuse_count, date)
                SELECT ?, 1, 0, ? 
                WHERE NOT EXISTS (SELECT 1 FROM nuke_table WHERE username = ?)
            """
    db_execute_query(query, (str(username), today, str(username)) )
    return True if is_repeat else False


def update_defuse_count(username):
    today = datetime.date.today()
    query = """INSERT INTO nuke_table (username, nuke_count, defuse_count, date)
            SELECT ?, 0, 1, ? 
            WHERE NOT EXISTS (SELECT 1 FROM nuke_table WHERE username = ?)
        """
    db_execute_query(query, (str(username), today, str(username)))


def query_nuke_count():
    nuke_cnt = db_select_one("SELECT SUM(nuke_count) FROM nuke_table")
    defuse_cnt = db_select_one("SELECT SUM(defuse_count) FROM nuke_table")

    nuke_total = nuke_cnt[0] if nuke_cnt and nuke_cnt[0] else 0
    defuse_total = defuse_cnt[0] if defuse_cnt and defuse_cnt[0] else 0
    return nuke_total - defuse_total


def query_nuke_last_date():
    result = db_select_one("SELECT date FROM nuke_table ORDER BY date DESC LIMIT 1")
    return result[0] if result else None


def insert_nickname(username, nickname):
    print(f"username{username}")
    print(f"nickname{nickname}")
    
    query = """INSERT INTO users (username, server_nick)
                VALUES (?, ?)
                ON CONFLICT (username) 
                DO UPDATE SET server_nick = excluded.server_nick;
            """
    
    db_execute_query(query, (str(username), nickname))

def get_nickname(username):
    print(username)

    query = """SELECT server_nick FROM users WHERE username = ?"""
    return db_select_one(query, (str(username),) )