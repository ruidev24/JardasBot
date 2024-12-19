import sqlite3
import random

def get_highscores():
    conn = sqlite3.connect("wordstats.db")
    c = conn.cursor()
    c.execute(
        "SELECT * FROM russian_roulette_score ORDER BY best_score DESC LIMIT 3",
    )
    podium = c.fetchall()

def reset_russian_curr_score(username):
    conn = sqlite3.connect("wordstats.db")
    c = conn.cursor()
    c.execute(
        "UPDATE mention_table SET current_score = ? WHERE username = ?",
        (0, username),
    )
    conn.commit()
    conn.close()

def update_russian_curr_score(username):
    query_check = "SELECT best_score, current_score FROM russain_roulette_score WHERE username = ?"
    conn = sqlite3.connect("wordstats.db")
    c = conn.cursor()
    c.execute(query_check, (username,))
    existing_user = c.fetchone()

    if existing_user is None:
        c.execute(
            "INSERT INTO mention_table (username, current_score) VALUES (?, ?)",
            (username, 1),
        )
    else:
        best_score = existing_user[0]
        curr_score = existing_user[1] + 1
        c.execute(
            "UPDATE mention_table SET current_score = ? WHERE username = ?",
            (curr_score, username),
        )

        if curr_score > best_score:
            c.execute(
                "UPDATE mention_table SET best_score = ? WHERE username = ?",
                (curr_score, username),
            )

    conn.commit()
    conn.close()