import sqlite3
import random

#################################################
def query_strangers_vocabulary():
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        c.execute("SELECT * FROM vocabulary_table")
        vocabulary_item = c.fetchall()
        conn.commit()

        return random.choice(vocabulary_item)[0]

    except sqlite3.Error as e:
        print("Error querying mention_cnt:", e)
    finally:
        conn.close()

#################################################
def query_mention_count(username):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        c.execute("SELECT * FROM mention_table WHERE username = ?", (username,))
        mention_item = c.fetchone()

        if mention_item:
            mention_cnt = mention_item[1]
        conn.commit()

        print(f'mention_cnt {mention_cnt}')
        return mention_cnt

    except sqlite3.Error as e:
        print("Error querying mention_cnt:", e)
    finally:
        conn.close()

#################################################
def query_nuke_count():
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        c.execute("SELECT SUM(nuke_count) FROM nuke_table")
        nuke_cnt = c.fetchone()[0]

        c.execute("SELECT SUM(defuse_count) FROM nuke_table")
        defuse_cnt = c.fetchone()[0]

        conn.commit()

        final_cnt = 0
        if nuke_cnt:
            final_cnt = nuke_cnt
        if nuke_cnt and defuse_cnt:
            final_cnt = nuke_cnt - defuse_cnt

        return final_cnt

    except sqlite3.Error as e:
        print("Error querying nuke_last_date:", e)
    finally:
        conn.close()

#################################################
def query_nuke_last_date():
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        c.execute("SELECT * FROM nuke_table ORDER BY date DESC LIMIT 1")
        nuke_item = c.fetchone()
        print("**")
        print(nuke_item)

        conn.commit()

        if nuke_item is not None:
            return nuke_item[3] # date
        
    except sqlite3.Error as e:
        print("Error querying nuke_last_date:", e)
    finally:
        conn.close()

#################################################
def query_leastFavourable():
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        c.execute("SELECT * FROM favour_table ORDER BY favour ASC LIMIT 1")
        favour_item = c.fetchone()
        conn.commit()

        if favour_item is not None:
            username = favour_item[0]

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user_item = c.fetchone()

        if user_item:
            return user_item[0] # server nickname
        
    except sqlite3.Error as e:
        print("Error querying least_favourable:", e)
    finally:
        conn.close()