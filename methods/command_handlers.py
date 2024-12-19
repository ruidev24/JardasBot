import random
import datetime
from datetime import timedelta
from discord import Message
from discord.ext import commands

from database import DBdelete
from database import DBupdate
from database import DBquery
from database import DBbotvars
from database import DBnew


from methods.response_handlers import (
    respond_acordar, 
    respond_sleep, 
    respond_self_roast,
    respond_roast,
    respond_defuse,
    respond_nuke,
    respond_fortune,
    respond_vocabulary)

from utils.state import STATE


async def handle_wakeup(message):
    DBupdate.update_positiveFavour(str(message.author))
    state = DBbotvars.get_state()
    if state == STATE.SLEEP:
        await respond_acordar(message)
        DBbotvars.update_state(STATE.NORMAL)
    else:
        await message.channel.send("Já tou acordado caralho, cala-te")



async def handle_sleep(message: Message):
    DBupdate.update_negativeFavour(str(message.author))
    await respond_sleep(message)
    DBbotvars.update_state(STATE.SLEEP)



async def handle_roast(bot: commands.bot, message: Message):
    mentioned_users = message.mentions
    if bot.user.mentioned_in(message):
        await respond_self_roast(message)
    elif mentioned_users:
        await respond_roast(message)
    else:
        await message.channel.send("Dou roast a quem? Seu burro!")




async def handle_intensity(value: str):
    value = int(value)
    if value >= 1 and value <= 4:
        intensity = value

    return intensity



async def handle_nuke(message):
    today = datetime.date.today()
    last_date = DBquery.query_nuke_last_date()
    if str(last_date) != str(today):
        DBdelete.clear_nuke_table()

    prev_cnt = DBquery.query_nuke_count()
    DBupdate.update_nuke_count(str(message.author))
    counter = DBquery.query_nuke_count()

    if counter == prev_cnt:
        await message.channel.send("Não há repeats")
    else:
        DBupdate.update_negativeFavour(str(message.author))

    if counter % 10 == 0:
        await nuke_channel(message)
    else:
        await respond_nuke(message)


# TODO
async def handle_highscores(message: Message):
    DBnew.get_highscores()
    print("highscores or something")


async def handle_russian_roulette(message: Message):
    bullet = random.randint(1, 6)
    DBnew.update_russian_curr_score(message.author)

    if bullet == 1:
        try:
            timeout_duration = timedelta(hours=1)
            await message.author.timeout(timeout_duration, reason="Drawn the bullet in Russian Roulette")
            await message.channel.send(f"{message.author.mention} has died")
        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")
    else:
        await message.channel.send(f"{message.author.mention} is safe!")

        


async def handle_hard_russian_roulette(message: Message):
    bullet = random.randint(0, 2)
    if not bullet:
        await message.channel.send(f"{message.author.mention} is safe!")
    else:
        try:
            timeout_seconds = random.randint(600, 10800)
            timeout_duration = timedelta(seconds=timeout_seconds)
            await message.author.timeout(timeout_duration, reason="Drawn the bullet in Russian Roulette")
            await message.channel.send(f"{message.author.mention} has died")
        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")


async def handle_death_roll(message: Message):
    old_death_roll = DBbotvars.get_death_roll()
    print(f"old_death_roll={old_death_roll}")

    curr_death_roll = random.randint(1, old_death_roll)
    print(f"curr_death_roll={curr_death_roll}")

    await message.channel.send(f"Deathroll = {curr_death_roll}")

    if curr_death_roll == 1:
        try:
            timeout_duration = timedelta(hours=3)
            await message.author.timeout(timeout_duration, reason="Drawn the bullet in Deathroll")
            await message.channel.send(f"{message.author.mention} has died")
            DBbotvars.update_death_roll(100)

        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")
    else:
        await message.channel.send(f"{message.author.mention} is safe!")
        DBbotvars.update_death_roll(curr_death_roll)


async def handle_fortune(message:Message):
    await respond_fortune(message)



async def handle_vocabulary(ctx, arg):
    DBupdate.update_vocabulary(arg, str(ctx.author))
    respond_vocabulary(ctx)


async def nuke_channel(message, allowed_mentions):
    pass
    await message.channel.send("Nuke activated...")
    await message.channel.send("NOW I AM BECOME DEATH, THE DESTROYER OF WORLDS...")
    # time.sleep(5)


async def handle_defuse(message: Message):
    prev_cnt = DBquery.query_nuke_count()
    DBupdate.update_defuse_count(str(message.author))
    counter = DBquery.query_nuke_count()
    if counter == prev_cnt:
        await message.channel.send("Não há repeats")
    else:
        DBupdate.update_positiveFavour(str(message.author))
        await respond_defuse(message)

#####################################################

#################################################################
# Codigo do Leo

async def glock_roulette(message: Message):
    bullet = random.randint(1, 99)
    if bullet != 1:
        try:
            timeout_duration = timedelta(minutes=10)
            await message.author.timeout(timeout_duration, reason="Drawn the bullet with a gun.")
            await message.channel.send(f"{message.author.mention} has died")
        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")
    else:
        await message.channel.send(f"{message.author.mention} is safe! The gun jammed.")

async def call_JECS(message: Message):
    if str(message.author) == "leomarcuzzo":
        try:
            await message.channel.send("<@192306440315076608> anda cá.")
            await message.channel.send("<@192306440315076608> anda cá.")
            await message.channel.send("<@192306440315076608> anda cá.")
        except Exception as e:
            await message.channel.send("Error sending message: {e}")
    else:
        pass

async def callKika(message: Message):
    if str(message.author) == "leomarcuzzo":
        try:
            await message.channel.send("<@402215966169235466> desenvolva-me.")
        except Exception as e:
            await message.channel.send("Error sending message: {e}")
    else:
        pass
