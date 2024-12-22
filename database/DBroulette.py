from database.DBhelpers import db_execute_query, db_select_all, db_select_one

def get_highscores_russian():
    return db_select_all("""SELECT us.server_nick, hs.best_score_russian 
                            FROM high_scores hs
                            JOIN users us ON hs.username = us.username
                            ORDER BY best_score_russian DESC 
                            LIMIT 3""")


def get_highscores_hardcore():
    return db_select_all("""SELECT us.server_nick, hs.best_score_hardcore 
                            FROM high_scores hs
                            JOIN users us ON hs.username = us.username
                            ORDER BY best_score_hardcore DESC 
                            LIMIT 3""")



def get_highscores_glock():
    return db_select_all("""SELECT us.server_nick, hs.best_score_glock 
                            FROM high_scores hs
                            JOIN users us ON hs.username = us.username
                            ORDER BY best_score_glock DESC 
                            LIMIT 3""")


def reset_russian_curr_score(username):
    query = """UPDATE high_scores SET curr_score_russian = ? WHERE username = ?"""
    db_execute_query(query, (0, str(username)))


def reset_hardcore_curr_score(username):
    query = """UPDATE high_scores SET curr_score_hardcore = ? WHERE username = ?"""
    db_execute_query(query, (0, str(username)))

    
def reset_glock_curr_score(username):
    query = """UPDATE high_scores SET curr_score_glock = ? WHERE username = ?"""
    db_execute_query(query, (0, str(username)))


def update_russian_score(username):
    query = """SELECT best_score_russian, curr_score_russian FROM high_scores WHERE username = ?"""
    response = db_select_one(query, (str(username),))

    if response is None:
        db_execute_query("INSERT INTO high_scores (username, best_score_russian, curr_score_russian) VALUES (?, ?, ?)", (str(username), 1, 1))
    else:
        best_score = response[0]
        curr_score = response[1] + 1
        db_execute_query("UPDATE high_scores SET curr_score_russian = ? WHERE username = ?", (curr_score, str(username)))

        if curr_score > best_score:
            db_execute_query("UPDATE high_scores SET best_score_russian = ? WHERE username = ?", (curr_score, str(username)))


def update_hardcore_score(username):
    query = """SELECT best_score_hardcore, curr_score_hardcore FROM high_scores WHERE username = ?"""
    response = db_select_one(query, (str(username),))

    if response is None:
        db_execute_query("INSERT INTO high_scores (username, best_score_hardcore, curr_score_hardcore) VALUES (?, ?, ?)", (str(username), 1, 1))
    else:
        best_score = response[0]
        curr_score = response[1] + 1
        db_execute_query("UPDATE high_scores SET curr_score_hardcore = ? WHERE username = ?", (curr_score, str(username)))

        if curr_score > best_score:
            db_execute_query("UPDATE high_scores SET best_score_hardcore = ? WHERE username = ?", (curr_score, str(username)))


def update_glock_score(username):
    query = """SELECT best_score_glock, curr_score_glock FROM high_scores WHERE username = ?"""
    response = db_select_one(query, (str(username),))

    if response is None:
        db_execute_query("INSERT INTO high_scores (username, best_score_glock, curr_score_glock) VALUES (?, ?, ?)", (str(username), 1, 1))
    else:
        best_score = response[0]
        curr_score = response[1] + 1
        db_execute_query("UPDATE high_scores SET curr_score_glock = ? WHERE username = ?", (curr_score, str(username)))

        if curr_score > best_score:
            db_execute_query("UPDATE high_scores SET best_score_glock = ? WHERE username = ?", (curr_score, str(username)))

