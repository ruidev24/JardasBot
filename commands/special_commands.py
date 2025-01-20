from discord.ext import commands
from methods.nuke_handlers import store_nicks
from database.DBbotvars import get_state
from utils.state import STATE
from methods.command_special_handlers import (
    handle_mistery,
    handle_huggies,
    handle_sacrifice,
    handle_list_events,
    handle_shrekt,
    handle_super_shrekt,
    call_JECS,
    callKika
)


def get_special_commands():
    special_commands = ["!mistery", "!huggies", "!sacrifice", "!get_shrekt", "!get_super_shrekt", "!list_events"]
    return special_commands


def setup_special_commands(bot: commands.Bot):
    
    @bot.command()
    async def mistery(ctx: commands.Context):
        print("DEBUG GUILD")
        print(ctx.channel.id)
        await store_nicks(ctx)
        await handle_mistery(ctx)

    @bot.command()
    async def huggies(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_huggies(ctx)

    # @bot.command()
    # async def sacrifice(ctx: commands.Context):
    #     await handle_sacrifice(ctx)

    # @bot.command()
    # async def get_shrekt(ctx: commands.Context):
    #     await handle_shrekt(ctx)

    # @bot.command()
    # async def get_super_shrekt(ctx: commands.Context, arg: str):
    #     await handle_super_shrekt(ctx, arg)

    # @bot.command()
    # async def list_events(ctx: commands.Context):
    #     await handle_list_events(ctx)

    @bot.command()
    async def callJECS(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await call_JECS(ctx)


    @bot.command()
    async def callKikaDev(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await callKika(ctx)


