import datetime
from discord import Message
from discord.ext import commands

from database import DBgeneral
from database import DBbotvars
from utils.state import STATE

from methods.response_handlers import (
    respond_acordar, 
    respond_sleep, 
    respond_self_roast,
    respond_roast,
    respond_fortune,
    respond_vocabulary
)

    

async def handle_wakeup(ctx: commands.Context):
    DBgeneral.update_positiveFavour(str(ctx.author))
    state = DBbotvars.get_state()
    if state == STATE.SLEEP:
        await respond_acordar(ctx)
        DBbotvars.update_state(STATE.NORMAL)
    else:
        await ctx.channel.send("Já tou acordado caralho, cala-te")


async def handle_sleep(ctx: commands.Context):
    DBgeneral.update_negativeFavour(str(ctx.author))
    await respond_sleep(ctx)
    DBbotvars.update_state(STATE.SLEEP)


async def handle_intensity(value: str):
    value = int(value)
    if value >= 1 and value <= 4:
        intensity = value
    return intensity


async def handle_mistery(ctx: commands.Context):
    await ctx.channel.send("Stuff was done")


async def handle_roast(bot: commands.bot, ctx: commands.Context):
    mentioned_users = ctx.mentions
    if bot.user.mentioned_in(ctx):
        await respond_self_roast(ctx)
    elif mentioned_users:
        await respond_roast(ctx)
    else:
        await ctx.channel.send("Dou roast a quem? Seu burro!")


async def handle_fortune(ctx: commands.Context):
    today = datetime.datetime.today().date()
    last_fortune = DBgeneral.get_last_fortune_timestamp(ctx.author)

    time_diff = today - last_fortune
    if time_diff > datetime.timedelta(days=7):
        await respond_fortune(ctx)
        DBgeneral.update_fortune(ctx.author)
    else:
        await ctx.channel.send("Só tens direito a 1 por semana caralho")


async def handle_vocabulary(ctx: commands.Context, arg):
    DBgeneral.update_vocabulary(arg, str(ctx.author))
    respond_vocabulary(ctx)


#################################################################
async def call_JECS(ctx: commands.Context):
    if str(ctx.author) == "leomarcuzzo":
        try:
            await ctx.channel.send("<@192306440315076608> anda cá.")
            await ctx.channel.send("<@192306440315076608> anda cá.")
            await ctx.channel.send("<@192306440315076608> anda cá.")
        except Exception as e:
            await ctx.channel.send("Error sending message: {e}")
    else:
        pass

    

async def callKika(ctx: commands.Context):
    if str(ctx.author) == "leomarcuzzo":
        try:
            await ctx.channel.send("<@402215966169235466> desenvolva-me.")
        except Exception as e:
            await ctx.channel.send("Error sending message: {e}")
    else:
        pass
