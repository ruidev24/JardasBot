import sqlite3
import datetime
from discord import Message

#################################################
def update_vocabulary(pvocabulary, pusername):
    print("HEY")
    print(pvocabulary)
    print(pusername)
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO vocabulary_table (vocabulary, username) VALUES (?, ?)",
            (pvocabulary, pusername),
        )

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating vocabulary_table:", e)
    finally:
        conn.close()


#################################################
def update_defuse_count(username):
    try:
        today = datetime.date.today()
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if user already exists
        c.execute("SELECT * FROM nuke_table WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user is None:
            c.execute(
                "INSERT INTO nuke_table (username, nuke_count, defuse_count, date) VALUES (?, 0, 1, ?)",
                (username, today),
            )

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating defuse_count:", e)
    finally:
        conn.close()


#################################################
def update_nuke_count(username):
    try:
        today = datetime.date.today()
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if user already exists
        c.execute("SELECT * FROM nuke_table WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user is None:
            c.execute(
                "INSERT INTO nuke_table (username, nuke_count, defuse_count, date) VALUES (?, 1, 0, ?)",
                (username, today),
            )

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating nuke_count:", e)
    finally:
        conn.close()


#################################################
def update_mention_cnt(username):
    try:
        today = datetime.date.today()
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if the user already exists
        c.execute("SELECT * FROM mention_table WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user is None:
            c.execute(
                "INSERT INTO mention_table (username, mention_cnt, date) VALUES (?, 1, ?)",
                (username, today),
            )
        else:
            count = existing_user[1] + 1
            c.execute(
                "UPDATE mention_table SET mention_cnt = ? WHERE username = ?",
                (count, username),
            )
            c.execute(
                "UPDATE mention_table SET date = ? WHERE username = ?",
                (today, username),
            )

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating mention_table:", e)
    finally:
        conn.close()


#################################################
def update_negativeFavour(username):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if the user already exists
        c.execute("SELECT * FROM favour_table WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user is None:
            c.execute(
                "INSERT INTO favour_table (username, favour) VALUES (?, -1)",
                (username,),
            )
        else:
            count = existing_user[1] - 1
            c.execute(
                "UPDATE favour_table SET favour = ? WHERE username = ?",
                (count, username),
            )

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating negative_favour:", e)
    finally:
        conn.close()


#################################################
def update_positiveFavour(username):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if the user already exists
        c.execute("SELECT * FROM favour_table WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user is None:
            c.execute(
                "INSERT INTO favour_table (username, favour) VALUES (?, 1)", (username,)
            )
        else:
            count = existing_user[1] + 1
            c.execute(
                "UPDATE favour_table SET favour = ? WHERE username = ?",
                (count, username),
            )

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating positive_favour:", e)
    finally:
        conn.close()


#################################################
def update_channel_words(channel, word):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if the channel exists
        c.execute("SELECT channel_id FROM channels WHERE channel_name = ?", (channel,))
        existing_channel = c.fetchone()

        if existing_channel:
            channel_id = existing_channel[0]

        # Check if the user-word association exists
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
    except sqlite3.Error as e:
        print("Error updating channel words:", e)
    finally:
        conn.close()


#################################################
def update_user_words(username, word):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if the user-word association already exists
        c.execute(
            "SELECT * FROM userwords WHERE username = ? AND word = ?", (username, word)
        )
        user_word = c.fetchone()

        if user_word is None:
            c.execute(
                "INSERT INTO userwords (username, word, count) VALUES (?, ?, 1)",
                (username, word),
            )
        else:
            count = user_word[2] + 1
            c.execute(
                "UPDATE userwords SET count = ? WHERE username = ? AND word = ?",
                (count, username, word),
            )

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating user words:", e)
    finally:
        conn.close()


#################################################
def update_words(word):
    print(word)
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if the word already exists
        c.execute("SELECT * FROM words WHERE word = ?", (word,))
        existing_word = c.fetchone()

        if existing_word is None:
            c.execute("INSERT INTO words (word, count) VALUES (?, 1)", (word,))
        else:
            count = existing_word[1] + 1
            c.execute("UPDATE words SET count = ? WHERE word = ?", (count, word))

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating word:", e)
    finally:
        conn.close()


#################################################
def update_users(message: Message):
    try:
        username = str(message.author)
        nick = str(message.author.nick)

        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if the user already exists
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = c.fetchone()

        if existing_user is None:
            c.execute(
                "INSERT INTO users (username, server_nick) VALUES (?, ?)",
                (username, nick),
            )

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating users:", e)
    finally:
        conn.close()


#################################################
def update_channels(message: Message):
    try:
        channel = str(message.channel)

        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Check if the channel already exists
        c.execute("SELECT * FROM channels WHERE channel_name = ?", (channel,))
        existing_channel = c.fetchone()

        if existing_channel is None:
            c.execute("INSERT INTO channels (channel_name) VALUES (?)", (channel,))

        conn.commit()
    except sqlite3.Error as e:
        print("Error updating channels:", e)
    finally:
        conn.close()
