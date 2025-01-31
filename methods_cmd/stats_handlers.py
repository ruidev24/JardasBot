from utils import stopfile
from database import DBstatistics, DBhelpers

from discord import Message
from discord.ext import commands
from tabulate import tabulate



#####################################################
async def update_stats(message: Message):
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

    if not top_words:
        await ctx.channel.send("Não há palavras registadas caralho.")
        return
    
    table = tabulate(top_words, headers=["Word", "Count"], tablefmt="simple_outline")
    
    await ctx.channel.send(f"The most used words in this discord server are:\n```\n{table}\n```")
    

async def get_top_words_by_user(ctx: commands.Context):
    mentioned_users = ctx.message.mentions

    for mentioned_user in ctx.message.mentions:
        username = DBstatistics.get_username_from_mention(mentioned_user.mention)
        if not username:
            return "That user doesn't exist"

        top_words_by_user = DBstatistics.get_top_words_by_user(username)

        if not top_words_by_user:
            await ctx.channel.send("Não há palavras registadas para este user caralho.")
            return
        
        table = tabulate(top_words_by_user, headers=["Word", "Count"], tablefmt="simple_outline")

        await ctx.channel.send(f"The most used words by this user are:\n```\n{table}\n```")



async def get_top_users_by_word(ctx: commands.Context, arg: str):
    word = arg.lower().replace(" ", "")
    word_id = DBstatistics.get_word_id(word)
    
    if not word_id:
        return "That words has never been written"
    
    top_users_by_word = DBstatistics.get_top_users_by_word(word_id)

    if not top_users_by_word:
        await ctx.channel.send("Não há palavras registadas para este user caralho.")
        return
    
    table = tabulate(top_users_by_word, headers=["username", "Count"], tablefmt="simple_outline")

    await ctx.channel.send(f"The users who most use this word are:\n```\n{table}\n```")


#####################################################################

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
