import datetime
import time
import random
import asyncio
import discord
from discord.ext import commands

from database import DBnuke
from database import DBgeneral
from methods.response_handlers import respond_defuse, respond_nuke, respond_bomb, respond_random_roast


##############################################################################
async def handle_nuke(bot: commands.Bot, ctx: commands.Context):
    allowed = DBnuke.query_nuke_allowed(ctx.author)
    if allowed:
        DBgeneral.update_negativeFavour(ctx.author)
    else:
        await ctx.channel.send("Não há repeats")
        return

    counter = DBnuke.query_nuke_count()
    if counter % 12 == 0:
        await nuke_channel(ctx)
    else:
        await respond_nuke(ctx)


async def handle_defuse(ctx: commands.Context):
    allowed = DBnuke.query_nuke_allowed(ctx.author)
    if allowed:
        DBgeneral.update_positiveFavour(ctx.author)
        await respond_defuse(ctx)
    else:
        await ctx.channel.send("Não há repeats")


async def nuke_channel(ctx: commands.Context):
    await store_nicks(ctx)
    await change_nicks(ctx)
    await drop_bombs(ctx)
    asyncio.sleep(60*10)
    await reset_nicks(ctx)


async def drop_bombs(ctx: commands.Context):
    await ctx.channel.send("Nuke activated...")
    time.sleep(1)

    count = 10
    while(count > 0):
        await ctx.channel.send(count)
        time.sleep(1)
        count -= 1

    await ctx.channel.send("NOW I AM BECOME DEATH, THE DESTROYER OF WORLDS...")
    for i in range(30):
        await respond_bomb(ctx)
        time.sleep(1)
        if random.randint(0, 1):
            await respond_random_roast(ctx)


async def store_nicks(ctx: commands.Context):
    if ctx.guild is None:
        return

    for member in ctx.guild.members:
        DBnuke.insert_nickname(member, member.display_name)
        

async def change_nicks(ctx: commands.Context):
    for member in ctx.guild.members:
        try:
            await member.edit(nick="everyone")
        except discord.Forbidden:
            print(f"Could not change {member.name}'s nickname (Missing permissions).")
        except discord.HTTPException as e:
            print(f"Error changing {member.name}'s nickname: {e}")


async def reset_nicks(ctx: commands.Context):
    for member in ctx.guild.members:
        try:
            nickname = DBnuke.get_nickname(member)
            await member.edit(nick=nickname)
        except discord.Forbidden:
            print(f"Could not change {member.name}'s nickname (Missing permissions).")
        except discord.HTTPException as e:
            print(f"Error changing {member.name}'s nickname: {e}")