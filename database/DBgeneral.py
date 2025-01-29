import sqlite3
import datetime
import random
from database.DBhelpers import db_execute_query, db_select_all, db_select_one


##############################################################################
def update_vocabulary(pvocabulary, pusername):
    query = "INSERT INTO vocabulary_table (vocabulary, username) VALUES (?, ?)"
    db_execute_query(query, (pvocabulary, pusername))


def get_mention_cnt(username) -> int:
    query = """SELECT mention_count FROM mention_bot_table WHERE username = ?"""
    result = db_select_one(query, (str(username),) )

    if result is None:
        query_insert = """INSERT INTO mention_bot_table (username, mention_count) VALUES (?, ?)"""
        db_execute_query(query_insert, (str(username), 0))
        return 0

    return result[0]


def update_mention_cnt(username):
    query = """INSERT INTO mention_bot_table (username, mention_count)
                VALUES (?, ?)
                ON CONFLICT (username) 
                DO UPDATE SET mention_count = mention_count + 1;
            """
    db_execute_query(query, (str(username), 1))


def reset_mention_table():
    query = """UPDATE mention_bot_table SET mention_count = 0"""
    db_execute_query(query)


def get_fortune_allowed(username) -> bool:
    query = """SELECT allowed FROM fortune_table WHERE username = ?"""
    result = db_select_one(query, (str(username),) )

    if result is None:
        query_insert = """INSERT INTO fortune_table (username, allowed) VALUES (?, ?)"""
        db_execute_query(query_insert, (str(username), True))
        return True

    return result[0]


def update_fortune_allowed(username):
    query = """INSERT INTO fortune_table (username, allowed)
                VALUES (?, ?)
                ON CONFLICT (username)
                DO UPDATE SET allowed = False
            """
    db_execute_query(query, (str(username), False) )


def reset_fortune_table():
    query = """UPDATE fortune_table SET has_asked = True"""
    db_execute_query(query)


def update_negativeFavour(username):
    query = """INSERT INTO favour_table (username, favour)
                VALUES (?, ?)
                ON CONFLICT (username) 
                DO UPDATE SET favour = favour - 1;
            """
    db_execute_query(query, (str(username), -1))


def update_positiveFavour(username):
    query = """INSERT INTO favour_table (username, favour)
                VALUES (?, ?)
                ON CONFLICT (username) 
                DO UPDATE SET favour = favour + 1;
            """
    db_execute_query(query, (str(username), 1))


def get_strangers_vocabulary() -> str:
    query = """SELECT vocabulary FROM vocabulary_table"""
    result = db_select_all(query)
    return random.choice(result)[0] if result else None


def get_least_favourable():
    query = """SELECT users.server_nick
                FROM users
                JOIN favour_table ON users.username = favour_table.username
                ORDER BY favour_table.favour ASC LIMIT 1
            """
    result = db_select_one(query)

    return result[0] if result else None


