import datetime
import time
import asyncio
import discord
from discord.ext import commands

from database import DBnuke
from database import DBgeneral
from methods.response_handlers import respond_defuse, respond_nuke, respond_bomb


async def handle_nuke(bot: commands.Bot, ctx: commands.Context):
    today = datetime.date.today()
    last_date = DBnuke.query_nuke_last_date()
    if str(last_date) != str(today):
        DBnuke.clear_nuke_table()

    is_repeat = DBnuke.update_nuke_count(ctx.author)
    if is_repeat:
        await ctx.channel.send("Não há repeats")
        return
    else:
        DBgeneral.update_negativeFavour(str(ctx.author))

    counter = DBnuke.query_nuke_count()
    # if counter % 12 == 0:
    if counter > 0:
        await nuke_channel(ctx)
    else:
        await respond_nuke(ctx)


async def handle_defuse(ctx: commands.Context):
    prev_cnt = DBnuke.query_nuke_count()
    DBnuke.update_defuse_count(str(ctx.author))
    counter = DBnuke.query_nuke_count()
    if counter == prev_cnt:
        await ctx.channel.send("Não há repeats")
    else:
        DBgeneral.update_positiveFavour(str(ctx.author))
        await respond_defuse(ctx)


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
    for i in range(40):
        await respond_bomb(ctx)
        time.sleep(2)


async def store_nicks(ctx: commands.Context):
    if ctx.guild is None:
        return

    for member in ctx.guild.members:
        DBnuke.insert_nickname(member, member.display_name)
        

async def change_nicks(ctx: commands.Context):
    for member in ctx.guild.members:
        try:
            # Change each user's nickname to the provided string
            await member.edit(nick="hivemind")
        except discord.Forbidden:
            ctx.channel.send(f"Could not change {member.name}'s nickname (Missing permissions).")
        except discord.HTTPException as e:
            ctx.channel.send(f"Error changing {member.name}'s nickname: {e}")


async def reset_nicks(ctx: commands.Context):
    for member in ctx.guild.members:
        try:
            nickname = DBnuke.get_nickname(member)
            await member.edit(nick=nickname)
        except discord.Forbidden:
            ctx.channel.send(f"Could not change {member.name}'s nickname (Missing permissions).")
        except discord.HTTPException as e:
            ctx.channel.send(f"Error changing {member.name}'s nickname: {e}")
    else:
        await ctx.channel.send("You don't have permission to change nicknames.")