from discord import Message
from discord.ext import commands

from commands.base_commands import setup_base_commands, get_base_commands
from commands.general_commands import setup_general_commands, get_general_commands
from commands.nuke_commands import setup_nuke_commands, get_nuke_commands
from commands.roulette_commands import setup_roulette_commands, get_roulette_commands
from commands.special_commands import setup_special_commands, get_special_commands
from commands.stat_commands import setup_stat_commands, get_stat_commands
from utils import utils

import sqlite3

##############################################################################
def is_command(message: Message):
    commands = []

    commands += get_base_commands()
    commands += get_general_commands()
    commands += get_nuke_commands()
    commands += get_roulette_commands()
    # commands += get_special_commands()
    commands += get_stat_commands()

    return any(command in str(message.content) for command in commands) 


def setup_commands(bot: commands.Bot):
    
    setup_base_commands(bot)
    setup_general_commands(bot)
    setup_nuke_commands(bot)
    setup_roulette_commands(bot)
    # setup_special_commands(bot)
    setup_stat_commands(bot)

    @bot.command()
    async def mistery(ctx: commands.Context):
        await utils.get_history_all_channels(ctx.guild)
        await ctx.channel.send("Francesinhas é tops caralho!")

    @bot.command()
    async def pasta(ctx: commands.Context):
        print("spaguetti")
        try:
            for member in ctx.guild.members:
                print("x")
                username = str(member)
                nick = str(member.nick) if member.nick else username
                mention = member.mention
                print(mention)
                query = """INSERT INTO users (username, server_nick, mention)
                            VALUES (?, ?, ?)
                            ON CONFLICT (username)
                            DO NOTHING
                        """
                
                params = (username, nick, mention)

                try:
                    conn = sqlite3.connect("wordstats_new.db")
                    c = conn.cursor()
                    c.execute(query, params)
                    conn.commit()
                except sqlite3.Error as e:
                    print("Database error:", e)
                finally:
                    conn.close()

        except Exception as e:
            print("Error:", e)


    @bot.command()
    async def meatballs(ctx: commands.Context):
        query = """SELECT mention FROM users LIMIT 1"""

        try:
            conn = sqlite3.connect("wordstats_new.db")
            c = conn.cursor()
            c.execute(query)
            x =  c.fetchone()
            await ctx.channel.send(f"{x[0]} desenvolva-me.")
        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            conn.close()
