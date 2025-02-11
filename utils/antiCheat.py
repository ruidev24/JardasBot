import discord
import random
import time
from datetime import timedelta

from database import DBcheats
from utils import stopfile
from collections import defaultdict
from responses import Cheats


#####################################################
async def handle_cheats(message: discord.Message):
    is_cheating = await check_for_cheats(message)

    if is_cheating == True:
        try:
            timeout_duration = timedelta(minutes=1)
            await message.author.timeout(timeout_duration, reason="Has tried to cheat the bot in stats")
            await respond_cheats(message)
        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")

    return is_cheating


async def check_for_cheats(message: discord.Message):
    #if await detect_spam_message(message):
    #    return True
    #if await detect_rapid_spamming(message):
    #    return True
    return False


async def detect_rapid_spamming(message: discord.Message):
    username = str(message.author)
    message_text = str(message.content).lower()
    words = message_text.split()

    for word in words:
        word = word.lower()
        if not stopfile.validate_word(word):
            continue

        first_time = DBcheats.get_cheat_timestamp(username, word)
        cheat_count = DBcheats.get_cheat_count(username, word)
        if not first_time:
            DBcheats.update_cheat_timestamp(username, word)
            continue

        time_diff = time.time() - first_time

        if time_diff < 60 and cheat_count > 5:
            DBcheats.correct_cheats(username, word, cheat_count)
            return True
        if time_diff > 60:
            DBcheats.update_cheat_timestamp(username, word)
        
    return False
            
        
async def detect_spam_message(message: discord.Message):
    message_text = str(message.content).lower()
    words = message_text.split()

    stats = defaultdict(int)
    for word in words:
        stats[word] += 1

        if stats[word] > 10:
            return True

    return False
    

async def respond_cheats(message: discord.Message):
    response = random.choice(Cheats.arr_cheats)
    await message.channel.send(response)
