import sqlite3
import datetime
import random
from database.DBhelpers import db_execute_query, db_select_all, db_select_one


##############################################################################
def update_vocabulary(pvocabulary, pusername):
    query = "INSERT INTO vocabulary_table (vocabulary, username) VALUES (?, ?)"
    db_execute_query(query, (pvocabulary, pusername))


def update_mention_cnt(username):
    today = datetime.date.today()
    query_check = "SELECT mention_cnt FROM mention_table WHERE username = ?"
    existing_user = db_select_one(query_check, (username,))


    if existing_user is None:
        db_execute_query("INSERT INTO mention_table (username, mention_cnt, date) VALUES (?, 1, ?)", (username, today) )
    else:
        count = existing_user[0] + 1
        db_execute_query("UPDATE mention_table SET mention_cnt = ?, date = ? WHERE username = ?", (count, today, username) )



def update_negativeFavour(username):
    query = """INSERT INTO favour_table (username, favour)
                SELECT ?, -1 WHERE NOT EXISTS (SELECT 1 FROM favour_table WHERE username = ?)
            """
    db_execute_query(query, (str(username), str(username)) )


def update_positiveFavour(username):
    query = """INSERT INTO favour_table (username, favour)
                SELECT ?, 1 WHERE NOT EXISTS (SELECT 1 FROM favour_table WHERE username = ?)
            """
    db_execute_query(query, (username, username))



def clear_mention_table(username: str):
    query = "DELETE FROM mention_table WHERE username = ?"
    db_execute_query(query, (username,))


def clear_database():
    queries = [
        "DELETE FROM users",
        "DELETE FROM channels",
        "DELETE FROM words",
        "DELETE FROM userwords",
        "DELETE FROM channelwords"
    ]
    for query in queries:
        db_execute_query(query)
    print("Tables deleted successfully.")


def get_fortune_allowed(username):
    allowed = db_select_one("SELECT allowed FROM fortunes_table WHERE username = ?", (str(username),) )
    return allowed[0] if allowed else False

def update_fortune_allowed(username):
    db_execute_query("UPDATE fortunes_table SET allowed = False WHERE username = ?", (str(username),) )

def reset_fortune():
    db_execute_query("UPDATE fortunes_table SET has_asked = True")



def query_strangers_vocabulary():
    result = db_select_all("SELECT vocabulary FROM vocabulary_table")
    return random.choice(result)[0] if result else None


def query_mention_count(username):
    result = db_select_one("SELECT mention_cnt FROM mention_table WHERE username = ?", (username,) )
    if result:
        return result[0]
    return 0




def query_mention_last_date(username):
    result = db_select_one("SELECT * FROM mention_table WHERE username = ?", (username,) )
    if result:
        return result[2]  # Assuming the date is in the 3rd column
    return None


def query_least_favourable():
    least_favourable = db_select_one("SELECT * FROM favour_table ORDER BY favour ASC LIMIT 1")
    if least_favourable:
        username = least_favourable[0]
        user_item = db_select_one("SELECT * FROM users WHERE username = ?", (username,))
        if user_item:
            return user_item[0]  # Assuming server nickname is in the 1st column
    return None
