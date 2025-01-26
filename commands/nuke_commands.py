from discord.ext import commands
from database.DBbotvars import bot_is_sleeping
from methods_cmd.nuke_handlers import handle_nuke, handle_defuse


##############################################################################
def get_nuke_commands() -> list[str]:
    return ["!nuke", "!defuse"]


def setup_nuke_commands(bot: commands.Bot):

    @bot.command()
    async def nuke(ctx: commands.Context):
        if bot_is_sleeping(): return
        await handle_nuke(bot, ctx)


    @bot.command()
    async def defuse(ctx: commands.Context):
        if bot_is_sleeping: return
        await handle_defuse(ctx)