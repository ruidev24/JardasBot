import sqlite3

from utils import stopfile
from database import DBstatistics, DBhelpers

from discord import Message
from discord.ext import commands




#####################################################
def update_stats(message: Message):
    username = str(message.author)
    message_text = str(message.content).lower()
    channel = str(message.channel)

    DBstatistics.update_users(message)
    DBstatistics.update_channels(message)

    words = message_text.split()

    for word in words:
        word = word.lower()
        if not stopfile.validate_word(word):
            continue

        DBstatistics.update_words(word)
        DBstatistics.update_user_words(username, word)

        # DBstatistics.update_channel_words(channel, word)


async def get_top_words_general(ctx: commands.Context):
    top_words = DBstatistics.get_words()

    response = "The most used words in this discord server are:\n"
    response += "Word".ljust(15) + "Count\n"
    response += "-" * 20 + "\n"
    for word in top_words:
        response += word[0].ljust(15) + str(word[1]).rjust(5) + "\n"

    await ctx.channel.send(response)


async def get_top_words_by_user(message: Message, arg: str):
    username = arg.lower().replace(" ", "")
    user_id = DBstatistics.get_user_id(username)
    if not user_id:
        return "That user doesn't exist"

    top_words_by_user = DBstatistics.get_top_words_by_user(user_id)

    response = "The most used words by this user are:\n"
    response += "{:<30} {:<5}\n".format("Word", "Count")
    for word in top_words_by_user:
        response += "{:<30} {:<5}\n".format(word[0], word[1])

    await message.channel.send(response)



async def get_top_users_by_word(ctx: commands.Context, arg: str):
    word = arg.lower().replace(" ", "")
    word_id = DBstatistics.get_word_id(word)
    if not word_id:
        return "That words has never been written"
    
    top_users_by_word = DBstatistics.get_top_users_by_word(word_id)

    response = "The users that most use this word are:\n"
    response += "{:<30} {:<5}\n".format("User", "Count")
    for user in top_users_by_word:
        response += "{:<30} {:<5}\n".format(user[0], user[1])

    await ctx.channel.send(response)




async def get_top_words_by_channel(ctx: commands.Context, arg: str):
    channel = arg.lower().replace(" ", "")
    channel_id = DBstatistics.get_channel_id(channel)
    if not channel_id:
        return "That channel doesn't exist"
    
    top_words_by_channel = DBstatistics.get_top_words_by_channel(channel)

    response = "The most used words written in this channel are:\n"
    response += "{:<30} {:<5}\n".format("Word", "Count")
    for word in top_words_by_channel:
        response += "{:<30} {:<5}\n".format(word[0], word[1])

    await ctx.channel.send(response)






def transform_channel(channel):
    query = """SELECT channel_name FROM channels"""
    all_channels = DBhelpers.db_select_all(query)

    for ch in all_channels:
        ch_str = ch[0]
        if channel in ch_str:
            return ch_str

    return channel
