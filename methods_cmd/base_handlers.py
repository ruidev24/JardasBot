from discord.ext import commands

from utils.state import STATE
from database import DBgeneral, DBbotvars
from methods.response_handlers import (
    respond_acordar, 
    respond_sleep
)

##############################################################################
async def handle_wakeup(ctx: commands.Context):
    DBgeneral.update_positiveFavour(str(ctx.author))
    state = DBbotvars.get_state()
    if STATE(state) == STATE.SLEEP:
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
        DBbotvars.update_intensity(value)


async def handle_status(ctx: commands.Context):
    state = DBbotvars.get_state()
    intensity = DBbotvars.get_intentsity()
    nuke_cnt = DBbotvars.get_nuke_cnt()
    message_str = f"state = {STATE(state)}\nintensity = {intensity}\nnuke count = {nuke_cnt}"
    await ctx.channel.send(message_str)



