import sqlite3

from utils import stopfile
from database import DBstatistics
from discord import Message

#####################################################
def update_stats(message: Message):
    username = str(message.author)
    message_text = str(message.content).lower()
    channel = str(message.channel)

    DBstatistics.update_users(message)
    DBstatistics.update_channels(message)

    words = message_text.split()

    for word in words:
        if not stopfile.validate_word(word):
            continue
        DBstatistics.update_words(word)
        DBstatistics.update_user_words(username, word)
        DBstatistics.update_channel_words(channel, word)


##################################################
async def get_top_users_by_word(message: Message):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        word = message.content[12:]
        word = word.lower()
        word = word.replace(" ", "")
        print(word)

        # Check if the word exists
        c.execute("SELECT word FROM words WHERE word = ?", (word,))
        word_id = c.fetchone()
        if not word_id:
            return "That words has never been written"

        # Query to get the top 10 words by user
        c.execute(
            """
            SELECT u.username, uw.count
            FROM userwords uw
            JOIN words w ON uw.word_id = w.word_id
            JOIN users u ON uw.user_id = u.user_id
            WHERE w.word = ?
            ORDER BY uw.count DESC
            LIMIT 10
        """,
            (word,),
        )

        top_users_by_word = c.fetchall()

        response = "The users that most use this word are:\n"
        response += "{:<30} {:<5}\n".format("User", "Count")
        for user in top_users_by_word:
            response += "{:<30} {:<5}\n".format(user[0], user[1])

        await message.channel.send(response)

    except sqlite3.Error as e:
        print("Error retrieving top words by user:", e)
    finally:
        conn.close()


#########################################
async def get_top_words_by_channel(message: Message):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        channel = message.content[15:]
        channel = channel.lower()
        channel = channel.replace(" ", "")
        channel = transform_channel(channel)
        print(channel)

        # Check if the channel exists
        c.execute("SELECT channel_id FROM channels WHERE channel_name = ?", (channel,))
        channel_id = c.fetchone()
        if not channel_id:
            return "That channel doesn't exist"

        # Query to get the top 10 words by channel
        c.execute(
            """
            SELECT w.word, cw.count
            FROM channelwords cw
            JOIN words w ON cw.word_id = w.word_id
            JOIN channels c ON cw.channel_id = c.channel_id
            WHERE c.channel_name = ?
            ORDER BY cw.count DESC
            LIMIT 10
        """,
            (channel,),
        )

        top_words_by_channel = c.fetchall()

        response = "The most used words written in this channel are:\n"
        response += "{:<30} {:<5}\n".format("Word", "Count")
        for word in top_words_by_channel:
            response += "{:<30} {:<5}\n".format(word[0], word[1])

        await message.channel.send(response)

    except sqlite3.Error as e:
        print("Error retrieving top words by channel:", e)
    finally:
        conn.close()


##################################################
async def get_top_words_by_user(message: Message):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        username = message.content[12:]
        username = username.lower()
        username = username.replace(" ", "")
        print(username)

        # Check if the user exists
        c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = c.fetchone()
        if not user_id:
            return "That user doesn't exist"

        # Query to get the top 10 words by user
        c.execute(
            """
            SELECT w.word, uw.count
            FROM userwords uw
            JOIN words w ON uw.word_id = w.word_id
            JOIN users u ON uw.user_id = u.user_id
            WHERE u.username = ?
            ORDER BY uw.count DESC
            LIMIT 10
        """,
            (username,),
        )

        top_words_by_user = c.fetchall()

        response = "The most used words by this user are:\n"
        response += "{:<30} {:<5}\n".format("Word", "Count")
        for word in top_words_by_user:
            response += "{:<30} {:<5}\n".format(word[0], word[1])

        await message.channel.send(response)

    except sqlite3.Error as e:
        print("Error retrieving top words by user:", e)
    finally:
        conn.close()


################################################
async def get_top_words_general(message: Message):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Query to get the top 10 words with the highest count
        c.execute("SELECT word, count FROM words ORDER BY count DESC LIMIT 10")
        top_words = c.fetchall()

        conn.commit()

        response = "The most used words in this discord server are:\n"
        response += "Word".ljust(15) + "Count\n"
        response += "-" * 20 + "\n"
        for word in top_words:
            response += word[0].ljust(15) + str(word[1]).rjust(5) + "\n"

        await message.channel.send(response)

    except sqlite3.Error as e:
        print("Error retrieving top words:", e)
    finally:
        conn.close()


#######################################################
def transform_channel(channel):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        c.execute("SELECT channel_name FROM channels")
        all_channels = c.fetchall()

        for ch in all_channels:
            ch_str = ch[0]
            if channel in ch_str:
                return ch_str
    except Exception as e:
        print("Error:", e)

    return channel
