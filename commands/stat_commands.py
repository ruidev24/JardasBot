from discord.ext import commands
from methods_cmd import stats_handlers
from database import DBstatistics


##############################################################################
def get_stat_commands():
    stat_commands = ["!stats", "!stats_uset", "!stats_words", "!stats_channel"]
    return stat_commands



def setup_stat_commands(bot: commands.Bot):

    @bot.command()
    async def stats(ctx: commands.Context):
        await stats_handlers.get_top_words_general(ctx)


    @bot.command()
    async def stats_user(ctx: commands.Context, arg):
        print(arg)
        await stats_handlers.get_top_words_by_user(ctx, arg)


    @bot.command()
    async def stats_word(ctx: commands.Context, arg):
        await stats_handlers.get_top_users_by_word(ctx, arg)


    @bot.command()
    async def stats_channel(ctx: commands.Context, arg):
        await stats_handlers.get_top_words_by_channel(ctx, arg)
