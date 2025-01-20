from discord.ext import commands
from database.DBbotvars import get_state
from utils.state import STATE
from methods.nuke_handlers import handle_nuke, handle_defuse
from methods.command_handlers import (
    handle_roast,
    handle_fortune,
    handle_vocabulary
)




def get_general_commands():
    special_commands = ["!mistery", "!huggies", "!sacrifice", "!get_shrekt", "!get_super_shrekt", "!list_events"]
    return special_commands


def setup_general_commands(bot: commands.Bot):
       # Nukes ###########################################
    @bot.command()
    async def nuke(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_nuke(bot, ctx)


    @bot.command()
    async def defuse(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_defuse(ctx)


    # General ##########################################
    @bot.command()
    async def roast(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_roast(bot, ctx)


    @bot.command()
    async def fortuneteller(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_fortune(ctx)


    @bot.command()
    async def vocabulary(ctx: commands.Context, arg):
        await handle_vocabulary(ctx, arg)