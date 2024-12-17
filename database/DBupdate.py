import sqlite3
import datetime
from discord import Message


def execute_db_query(query: str, params: tuple = ()):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print("Database error:", e)
    finally:
        conn.close()


def update_vocabulary(pvocabulary, pusername):
    query = "INSERT INTO vocabulary_table (vocabulary, username) VALUES (?, ?)"
    execute_db_query(query, (pvocabulary, pusername))


def update_defuse_count(username):
    today = datetime.date.today()
    query = """
        INSERT INTO nuke_table (username, nuke_count, defuse_count, date)
        SELECT ?, 0, 1, ? 
        WHERE NOT EXISTS (SELECT 1 FROM nuke_table WHERE username = ?)
    """
    execute_db_query(query, (username, today, username))


def update_nuke_count(username):
    today = datetime.date.today()
    query = """
        INSERT INTO nuke_table (username, nuke_count, defuse_count, date)
        SELECT ?, 1, 0, ? WHERE NOT EXISTS (SELECT 1 FROM nuke_table WHERE username = ?)
    """
    execute_db_query(query, (username, today, username))


#################################################
def update_mention_cnt(username):
    today = datetime.date.today()
    query_check = "SELECT mention_cnt FROM mention_table WHERE username = ?"
    conn = sqlite3.connect("wordstats.db")
    c = conn.cursor()
    c.execute(query_check, (username,))
    existing_user = c.fetchone()

    if existing_user is None:
        c.execute(
            "INSERT INTO mention_table (username, mention_cnt, date) VALUES (?, 1, ?)",
            (username, today),
        )
    else:
        count = existing_user[0] + 1
        c.execute(
            "UPDATE mention_table SET mention_cnt = ?, date = ? WHERE username = ?",
            (count, today, username),
        )

    conn.commit()
    conn.close()


def update_negativeFavour(username):
    query = """
        INSERT INTO favour_table (username, favour)
        SELECT ?, -1 WHERE NOT EXISTS (SELECT 1 FROM favour_table WHERE username = ?)
        """
    execute_db_query(query, (username, username))


def update_positiveFavour(username):
    query = """
        INSERT INTO favour_table (username, favour)
        SELECT ?, 1 WHERE NOT EXISTS (SELECT 1 FROM favour_table WHERE username = ?)
        """
    execute_db_query(query, (username, username))


def update_channel_words(channel, word):
    conn = sqlite3.connect("wordstats.db")
    c = conn.cursor()

    c.execute("SELECT channel_id FROM channels WHERE channel_name = ?", (channel,))
    existing_channel = c.fetchone()

    if existing_channel:
        channel_id = existing_channel[0]
        c.execute(
            "SELECT * FROM channelwords WHERE channel_id = ? AND word = ?",
            (channel_id, word),
        )
        channel_word = c.fetchone()

        if channel_word is None:
            c.execute(
                "INSERT INTO channelwords (channel_id, word, count) VALUES (?, ?, 1)",
                (channel_id, word),
            )
        else:
            count = channel_word[2] + 1
            c.execute(
                "UPDATE channelwords SET count = ? WHERE channel_id = ? AND word = ?",
                (count, channel_id, word),
            )

    conn.commit()
    conn.close()


# Update user word count
def update_user_words(username, word):
    query = """
        INSERT INTO userwords (username, word, count)
        SELECT ?, ?, 1 WHERE NOT EXISTS (SELECT 1 FROM userwords WHERE username = ? AND word = ?)
    """
    execute_db_query(query, (username, word, username, word))


# Update words count in general
def update_words(word):
    query = """
        INSERT INTO words (word, count)
        SELECT ?, 1 WHERE NOT EXISTS (SELECT 1 FROM words WHERE word = ?)
    """
    execute_db_query(query, (word, word))


# Update users table based on Discord message
def update_users(message: Message):
    username = str(message.author)
    nick = str(message.author.nick)
    query = """
        INSERT INTO users (username, server_nick)
        SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = ?)
    """
    execute_db_query(query, (username, nick, username))


#################################################
# Update channels table based on Discord message
def update_channels(message: Message):
    channel = str(message.channel)
    query = """
        INSERT INTO channels (channel_name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM channels WHERE channel_name = ?)
    """
    execute_db_query(query, (channel, channel))
