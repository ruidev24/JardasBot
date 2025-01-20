from discord.ext import commands
from database.DBbotvars import get_state
from utils.state import STATE
from methods_cmd.general_handlers import (
    handle_roast,
    handle_fortune,
    handle_vocabulary
)


##############################################################################


def get_general_commands():
    special_commands = ["!roast", "!fortuneteller", "!vocabulary"]
    return special_commands


def setup_general_commands(bot: commands.Bot):

    @bot.command()
    async def roast(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_roast(bot, ctx)


    @bot.command()
    async def fortuneteller(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_fortune(ctx)


    @bot.command()
    async def vocabulary(ctx: commands.Context, arg):
        await handle_vocabulary(ctx, arg)