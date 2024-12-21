import datetime
from discord import Message
from discord.ext import commands

from database import DBdelete
from database import DBupdate
from database import DBquery
from database import DBbotvars


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
