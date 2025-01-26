from discord.ext import commands
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
        await handle_roast(bot, ctx)


    @bot.command()
    async def fortuneteller(ctx: commands.Context):
        await handle_fortune(ctx)


    @bot.command()
    async def vocabulary(ctx: commands.Context, arg):
        await handle_vocabulary(ctx, arg)