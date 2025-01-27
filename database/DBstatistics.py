from discord import Message
from database.DBhelpers import db_execute_query, db_select_all, db_select_one


##############################################################################
def get_user_id(username: str):
    query = """SELECT username FROM users WHERE username = ?"""
    result = db_select_one(query, (username,))
    return result[0] if result else None


def get_word_id(word: str):
    query = """SELECT word FROM words WHERE word = ?"""
    result = db_select_one(query, (word,))
    return result[0] if result else None


def get_channel_id(channel: str):
    query = """SELECT channel_id FROM channels WHERE channel_name = ?"""
    result = db_select_one(query, (channel,))
    return result[0] if result else None


###############################################################################
def get_words():
    query = """SELECT word, count FROM words ORDER BY count DESC LIMIT 10"""
    result = db_select_all(query)
    return result


def get_top_words_by_user(user: str):
    query = """SELECT w.word, uw.count
                FROM user_words uw
                JOIN words w ON uw.word = w.word
                JOIN users u ON uw.username = u.username
                WHERE u.username = ?
                ORDER BY uw.count DESC
                LIMIT 10
            """
    result = db_select_all(query, (user,))
    return result[0] if result else None


def get_top_users_by_word(word: str):
    query = """SELECT u.username, uw.count
                FROM user_words uw
                JOIN words w ON uw.word = w.word
                JOIN users u ON uw.username = u.username
                WHERE w.word = ?
                ORDER BY uw.count DESC
                LIMIT 10
            """
    result = db_select_all(query, (word,))
    return result[0] if result else None

def get_top_words_by_channel(channel: str):
    query = """SELECT w.word, cw.count
                FROM channel_words cw
                JOIN words w ON cw.word = w.word
                JOIN channels c ON cw.channel_id = c.id
                WHERE c.name = ?
                ORDER BY cw.count DESC
                LIMIT 10
            """
    result = db_select_all(query, (channel,))
    return result[0] if result else None

    
####################################################################
def update_words(word: str):
    query = """INSERT INTO words (word, count)
                VALUES (?, 1)
                ON CONFLICT (word)
                DO UPDATE SET count = count + 1;
            """
    db_execute_query(query, (word,))


def update_users(message: Message):
    username = str(message.author)
    nick = str(message.author.nick) if message.author.nick else username  # Handle cases where nick might be None
    query = """INSERT INTO users (username, server_nick)
                VALUES (?, ?)
                ON CONFLICT (username)
                DO NOTHING
            """
    db_execute_query(query, (username, nick))


def update_channels(message: Message):
    channel = str(message.channel)
    query = """INSERT INTO channels (name)
                VALUES (?)
                ON CONFLICT (name)
                DO NOTHING
            """
    db_execute_query(query, (channel,))


def update_user_words(username, word):
    query = """INSERT INTO user_words (username, word, count)
                VALUES (?, ?, 1)
                ON CONFLICT (username, word)
                DO UPDATE SET count = count + 1;
            """
    db_execute_query(query, (username, word))


def update_channel_words(channel, word):
    existing_channel = db_select_one("SELECT channel_id FROM channels WHERE channel_name = ?", (channel,) )

    if not existing_channel:
        return
    
    channel_id = existing_channel[0]
    channel_word = db_select_one("SELECT * FROM channelwords WHERE channel_id = ? AND word = ?", (channel_id, word),)

    if channel_word is None:
        db_execute_query("INSERT INTO channelwords (channel_id, word, count) VALUES (?, ?, 1)", (channel_id, word),)
    else:
        count = channel_word[2] + 1
        db_execute_query("UPDATE channelwords SET count = ? WHERE channel_id = ? AND word = ?", (count, channel_id, word),)