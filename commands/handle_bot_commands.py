import time
from discord import Message
from discord.ext import commands

from commands.base_commands import setup_base_commands, get_base_commands
from commands.dev_commands import setup_dev_commands, get_dev_commands
from commands.general_commands import setup_general_commands, get_general_commands
from commands.nuke_commands import setup_nuke_commands, get_nuke_commands
from commands.roulette_commands import setup_roulette_commands, get_roulette_commands
from commands.special_commands import setup_special_commands, get_special_commands
from commands.stat_commands import setup_stat_commands, get_stat_commands



##############################################################################
def is_command(message: Message):
    commands = []

    commands += get_base_commands()
    commands += get_dev_commands()
    commands += get_general_commands()
    commands += get_nuke_commands()
    commands += get_roulette_commands()
    # commands += get_special_commands()
    commands += get_stat_commands()

    return any(command in str(message.content) for command in commands) 


def setup_commands(bot: commands.Bot):
    
    setup_base_commands(bot)
    setup_dev_commands(bot)
    setup_general_commands(bot)
    setup_nuke_commands(bot)
    setup_roulette_commands(bot)
    # setup_special_commands(bot)
    setup_stat_commands(bot)


    @bot.command()
    async def shadow(ctx: commands.Context):
        guild = ctx.guild  # Obter o servidor
        member = ctx.author  # A pessoa que usou o comando

        # Adicionar o cargo novo
        role_shadow = "Shadow Banned"  # Nome do cargo que será atribuído - tem de estar igual igual ao que está no discord!        
        role_novo = next((role for role in guild.roles if role.name == role_shadow), None)
        await member.add_roles(role_novo)
        await ctx.send(f"O cargo `{role_shadow}` foi atribuído a você!")

        # Remover o cargo antigo
        role_base = "membro"  # Nome do cargo a ser removido - tem de estar igual igual ao que está no discord!
        role_sai = next((role for role in guild.roles if role.name == role_base), None)
        await member.remove_roles(role_sai)
        await ctx.send(f"O cargo `{role_base}` foi removido.")

        time.sleep(2*60*60)

        # Após 2 horas, remover o cargo "Shadow Banned" e reatribuir o cargo "membro"
        await member.remove_roles(role_novo)
        await member.add_roles(role_sai)
        await ctx.send("Welcome back", member)       

