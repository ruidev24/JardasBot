from discord.ext import commands
from utils.state import STATE
from database.DBbotvars import get_state
from methods_cmd.nuke_handlers import handle_nuke, handle_defuse


##############################################################################
def get_nuke_commands():
    nuke_commands = ["!nuke", "!defuse"]
    return nuke_commands


def setup_nuke_commands(bot: commands.Bot):

    @bot.command()
    async def nuke(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_nuke(bot, ctx)


    @bot.command()
    async def defuse(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_defuse(ctx)