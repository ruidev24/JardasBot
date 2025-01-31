import discord
import random
import datetime

from collections import defaultdict

from methods_cmd import stats_handlers
from database import DBgeneral
from responses import Mentions
from responses import Cheats




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
