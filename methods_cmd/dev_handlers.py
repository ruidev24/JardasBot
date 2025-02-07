import discord
from discord.ext import commands
from database import DBdev
from methods_cmd.stats_handlers import update_stats

##############################################################################
async def handle_clean_data():
    DBdev.clean_data()

async def handle_clean_words():
    DBdev.clean_words()


async def handle_get_history(ctx: commands.Context):
    try:
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await get_history(channel)
    except Exception as e:
            print("Error:", e)

async def get_history(channel):
    try:
        async for message in channel.history():
            await update_stats(message)
    except Exception as e:
        print("Error:", e)


async def handle_get_guild_data(ctx: commands.Context):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            DBdev.update_channels(channel)

    for member in ctx.guild.members:
        await update_database_member(member)

    DBdev.setup_global_variables()

async def update_database_member(member):
    DBdev.update_users(member)
    DBdev.update_favour_table(member)
    DBdev.update_fortune_table(member)
    DBdev.update_highscores_table(member)
    DBdev.update_mention_bot_table(member)
    DBdev.update_nuke_table(member)

    


