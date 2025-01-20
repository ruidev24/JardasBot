from discord.ext import commands
from methods_cmd import stats_handlers


##############################################################################
def get_stat_commands():
    stat_commands = ["!stats", "!stats_uset", "!stats_words", "!stats_channel"]
    return stat_commands


def setup_stat_commands(bot: commands.Bot):

    @bot.command()
    async def stats(ctx):
        await stats_handlers.get_top_words_general(ctx.message)


    @bot.command()
    async def stats_user(ctx):
        await stats_handlers.get_top_words_by_user(ctx.message)


    @bot.command()
    async def stats_word(ctx):
        await stats_handlers.get_top_users_by_word(ctx.message)


    @bot.command()
    async def stats_channel(ctx):
        await stats_handlers.get_top_words_by_channel(ctx.message)
