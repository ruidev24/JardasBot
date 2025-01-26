import discord
import random
import datetime

from collections import defaultdict

from methods_cmd import stats_handlers
from database import DBgeneral
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
            stats_handlers.update_stats(message)
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
async def handle_mention(message: discord.Message):
    DBgeneral.update_mention_cnt(message.author)
    mention_cnt = DBgeneral.get_mention_cnt(message.author)

    if mention_cnt <= 7:
        await respond_mention_general(message)
    elif mention_cnt == 8:
        await message.channel.send("Ai queres festa? Já te fodo")
        await respond_mention_dm(message)
    else:
        await respond_mention_dm(message)



async def respond_mention_dm(message: discord.Message):
    response = random.choice(Mentions.arr_mention)
    dm = ( await message.author.create_dm() )
    await dm.send(response)


async def respond_mention_general(message: discord.Message):
    response = random.choice(Mentions.arr_mention)
    await message.channel.send(response)
