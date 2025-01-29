from discord.ext import commands
from methods_cmd.dev_handlers import (
    handle_get_guild_data,
    handle_get_history,
    handle_clean_data,
    handle_clean_words
)


##############################################################################
def get_dev_commands():
    dev_commmands = ["!get_guild_data", "!get_guild_history", "!clean_data", "clean_words"]
    return dev_commmands


def setup_dev_commands(bot: commands.Bot):
    @bot.command()
    async def get_guild_data(ctx: commands.Context):
        if str(ctx.author) != "ruimachado":
            await ctx.channel.send("Isto é só para devs")
            return

        print("get_guild_data")
        await handle_get_guild_data(ctx)
        await ctx.channel.send("Data retrieved")

    @bot.command()
    async def get_guild_history(ctx: commands.Context):
        if str(ctx.author) != "ruimachado":
            await ctx.channel.send("Isto é só para devs")
            return

        print("get_guild_history")
        await handle_get_history(ctx)
        await ctx.channel.send("History retrieved")

    @bot.command()
    async def clean_data(ctx: commands.Context):
        if str(ctx.author) != "ruimachado":
            await ctx.channel.send("Isto é só para devs")
            return
        
        print("clean_data")
        await handle_clean_data()
        await ctx.channel.send("Data cleaned")

    @bot.command()
    async def clean_words(ctx: commands.Context):
        if str(ctx.author) != "ruimachado":
            await ctx.channel.send("Isto é só para devs")
            return
        
        print("clean_words")
        await handle_clean_words()
        await ctx.channel.send("Words cleaned")

