import time
import asyncio
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
    async def remove(ctx: commands.Context):
        guild = ctx.guild
        role_remove = next((role for role in guild.roles if role.name == "Shadow Banned"), None)
        await ctx.author.remove_roles(role_remove)
        print("caralho")

    @bot.command()
    async def shadow(ctx: commands.Context):
        guild = ctx.guild  # Obter o servidor
        member = ctx.author  # A pessoa que usou o comando

        role_novo = next((role for role in guild.roles if role.name == "Shadow Banned"), None)
        role_membro = next((role for role in guild.roles if role.name == "membro"), None)

        try:
            await member.send("Quantos minutos precisas bebé?")
            def check(m):
                return m.author == member and m.content.isdigit()

            msg = await bot.wait_for("message", check=check, timeout=30) # Tens 30segundos para responder ao bot
            tempo_minutos = int(msg.content) * 60

            # Adicionar role novo, remover role membro
            await member.add_roles(role_novo)
            await member.remove_roles(role_membro)
            await member.send(f"You are now 'Shadow Banned'. Get to work, weakling")

            await asyncio.sleep(tempo_minutos)  # Espera assíncrona por 2 horas

            # Devolver o estado inicial
            await member.remove_roles(role_novo)
            await member.add_roles(role_membro)
            await ctx.send(f"Welcome back, {member.mention}")
    
        except asyncio.TimeoutError:
            await member.send("Demoraste bues a responder, tchau.")
            return
        
