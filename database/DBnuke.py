import datetime
from database.DBhelpers import db_execute_query, db_select_all, db_select_one


##############################################################################
def reset_nuke_table():
    query = """UPDATE nuke_table
               SET nuke_count = 0, 
               defuse_count = 0, 
               allowed = True
            """
    db_execute_query(query)


def update_nuke_count(username):
    query = """UPDATE nuke_table
               SET nuke_count = 1
               WHERE username = ?    
            """
    db_execute_query(query, (str(username),) )


def update_defuse_count(username):
    query = """UPDATE nuke_table
               SET defuse_count = 1
               WHERE username = ?    
            """
    db_execute_query(query, (str(username),) )


def insert_nuke_count(username):
    query = """INSERT INTO nuke_table (username)
                VALUES (?)
            """
    db_execute_query(query, (str(username),) )


def query_nuke_count():
    nuke_cnt = db_select_one("SELECT SUM(nuke_count) - SUM(defuse_count) FROM nuke_table")
    return nuke_cnt[0] if nuke_cnt and nuke_cnt[0] else 0


def query_nuke_allowed(username):
    query = """SELECT allowed FROM nuke_table WHERE username = ?"""
    return db_select_one(query, (str(username),) )


def insert_nickname(username, nickname):    
    query = """INSERT INTO users (username, server_nick)
                VALUES (?, ?)
                ON CONFLICT (username) 
                DO UPDATE SET server_nick = excluded.server_nick;
            """
    db_execute_query(query, (str(username), nickname))


def get_nickname(username):
    query = """SELECT server_nick FROM users WHERE username = ?"""
    nickname = db_select_one(query, (str(username),) )
    return nickname[0] if nickname else None