from database.DBhelpers import db_execute_query, db_select_all, db_select_one
import time

##############################################################################
def get_cheat_timestamp(username, word):
    query = """SELECT cheat_timestamp FROM user_words 
                WHERE username = ? AND word = ?"""
    
    result = db_select_one(query, (username, word))
    return result[0] if result else None


def get_cheat_count(username, word):
    query = """SELECT cheat_count FROM user_words 
                WHERE username = ? AND word = ?"""
    
    result = db_select_one(query, (username, word))
    return result[0] if result else None


def update_cheat_timestamp(username, word):
    query = """UPDATE user_words
                SET cheat_timestamp = ?
                WHERE username = ? AND word = ?"""
    
    timestamp = time.time()
    db_execute_query(query, (timestamp, username, word))


def correct_cheats(username, word, cheat_count):
    query1 = """UPDATE user_words
                SET count = count - ?,
                cheat_count = 0
                WHERE username = ? AND word = ?"""
    
    db_execute_query(query1, (cheat_count, username, word))

    query2 = """UPDATE words
                SET count = count - ?
                WHERE word = ?"""
    
    db_execute_query(query2, (cheat_count, word))