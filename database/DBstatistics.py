from discord import Message
from database.DBhelpers import db_execute_query, db_select_all, db_select_one


def update_words(word):
    query = """
        INSERT INTO words (word, count)
        SELECT ?, 1 WHERE NOT EXISTS (SELECT 1 FROM words WHERE word = ?)
    """
    db_execute_query(query, (word, word))


def update_users(message: Message):
    username = str(message.author)
    nick = str(message.author.nick)
    query = """
        INSERT INTO users (username, server_nick)
        SELECT ?, ? WHERE NOT EXISTS (SELECT 1 FROM users WHERE username = ?)
    """
    db_execute_query(query, (username, nick, username))


def update_channels(message: Message):
    channel = str(message.channel)
    query = """
        INSERT INTO channels (channel_name)
        SELECT ? WHERE NOT EXISTS (SELECT 1 FROM channels WHERE channel_name = ?)
    """
    db_execute_query(query, (channel, channel))


def update_user_words(username, word):
    query = """
        INSERT INTO userwords (username, word, count)
        SELECT ?, ?, 1 WHERE NOT EXISTS (SELECT 1 FROM userwords WHERE username = ? AND word = ?)
    """
    db_execute_query(query, (username, word, username, word))


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