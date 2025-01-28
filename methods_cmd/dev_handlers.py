import discord
from discord.ext import commands
from database import DBdev
from methods_cmd.stats_handlers import update_stats

##############################################################################
async def handle_get_history(ctx: commands.Context):
    for channel in ctx.guild.channels:
        if not isinstance(channel, discord.TextChannel):
            return
    
        for message in channel.history():
            update_stats(message)



async def handle_get_guild_data(ctx: commands.Context):
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            DBdev.update_channels(channel)

    for member in ctx.guild.members:
        update_database_member(member)


async def update_database_member(member):
    DBdev.update_users(member)
    DBdev.update_favour_table(member)
    DBdev.update_fortune_table(member)
    DBdev.update_highscores_table(member)
    DBdev.update_mention_bot_table(member)
    DBdev.update_nuke_table(member)

    


