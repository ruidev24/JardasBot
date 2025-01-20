from discord.ext import commands
from database.DBbotvars import get_state
from utils.state import STATE
from methods.command_handlers import (
    handle_wakeup,
    handle_sleep,
    handle_intensity,
    handle_status
)


def get_base_commands():
    base_commands = ["!acorda", "!vaidormir", "!intensity", "!status"]
    return base_commands


def setup_base_commands(bot: commands.Bot):

    @bot.command()
    async def acorda(ctx: commands.Context):
        await handle_wakeup(ctx)


    @bot.command()
    async def vaidormir(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_sleep(ctx)


    @bot.command()
    async def intensity(ctx: commands.Context, arg: str):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_intensity(arg)


    @bot.command()
    async def status(ctx: commands.Context):
        await handle_status(ctx)

