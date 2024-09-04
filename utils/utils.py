import discord
import random
import datetime

from collections import defaultdict

from methods import stats_handle
from database import DBquery
from database import DBupdate
from database import DBdelete
from responses import Mentions
from responses import Cheats


#####################################################
async def get_history_all_channels(guild):
    try:
        # Iterate over every channel in the server
        for channel in guild.channels:
            # Check if the channel is a text channel
            if isinstance(channel, discord.TextChannel):
                await get_history(
                    channel
                )  # Await the execution of asynchronous function
    except Exception as e:
        print("Error:", e)


async def get_history(channel):
    try:
        async for message in channel.history():
            stats_handle.update_stats(message)
    except Exception as e:
        print("Error:", e)


#####################################################
async def check_for_cheats(message: discord.Message):
    try:
        message_text = str(message.content).lower()
        words = message_text.split()

        stats = defaultdict(int)
        for word in words:
            stats[word] += 1

            if stats[word] > 10:
                await respond_cheats(message)
                return True

        return False
    except Exception as e:
        print("Error checking for cheats:", e)


async def respond_cheats(message: discord.Message):
    response = random.choice(Cheats.arr_cheats)
    await message.channel.send(response)


#####################################################
async def respond_mention(message: discord.Message):
    today = datetime.date.today()
    last_date = DBquery.query_mention_last_date(str(message.author))
    if str(last_date) != str(today):
        DBdelete.clear_mention_table(str(message.author))

    DBupdate.update_mention_cnt(str(message.author))
    mention_cnt = int(DBquery.query_mention_count(str(message.author)))

    if mention_cnt < 10:
        await respond_mention_general(message)
    elif mention_cnt == 10:
        await message.channel.send("Ai queres festa? Já te fodo")
    else:
        await respond_mention_dm(message)


async def respond_mention_dm(message: discord.Message):
    response = random.choice(Mentions.arr_mention)
    dm = (
        await message.author.create_dm()
    )  # If dm is already made, it does not matter :)
    await dm.send(response)


async def respond_mention_general(message: discord.Message):
    response = random.choice(Mentions.arr_mention)
    await message.channel.send(response)
