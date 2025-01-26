from discord import Message
from discord.ext import commands

from commands.base_commands import setup_base_commands, get_base_commands
from commands.general_commands import setup_general_commands, get_general_commands
from commands.nuke_commands import setup_nuke_commands, get_nuke_commands
from commands.roulette_commands import setup_roulette_commands, get_roulette_commands
from commands.special_commands import setup_special_commands, get_special_commands
from commands.stat_commands import setup_stat_commands, get_stat_commands


##############################################################################
def is_command(message: Message):
    commands = []

    commands += get_base_commands()
    commands += get_general_commands()
    commands += get_nuke_commands()
    commands += get_roulette_commands()
    # commands += get_special_commands()
    # commands += get_stat_commands()

    return any(command in str(message.content) for command in commands) 


def setup_commands(bot: commands.Bot):
    
    setup_base_commands(bot)
    setup_general_commands(bot)
    setup_nuke_commands(bot)
    setup_roulette_commands(bot)
    # setup_special_commands(bot)
    # setup_stat_commands(bot)

