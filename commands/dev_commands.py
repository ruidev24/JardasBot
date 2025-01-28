from discord.ext import commands
from methods_cmd.dev_handlers import (
    handle_get_guild_data
)


##############################################################################
def get_dev_commands():
    dev_commmands = ["get_guild_data"]
    return dev_commmands


def setup_dev_commands(bot: commands.Bot):
    @bot.command()
    async def get_guild_data(ctx: commands.Context):
        await handle_get_guild_data(ctx)
        await ctx.channel.send("Data retrieved")

    @bot.command()
    async def get_guild_history(ctx: commands.Context):
        await handle_get_guild_data(ctx)
        await ctx.channel.send("History retrieved")
