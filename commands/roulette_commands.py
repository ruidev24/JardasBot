from discord.ext import commands
from database.DBbotvars import get_state
from utils.state import STATE
from methods_cmd.roulette_handlers import (
    handle_russian_roulette, 
    handle_hardcore_roulette, 
    handle_glock_roulette, 
    handle_ak47_roulette, 
    handle_death_roll, 
    handle_highscores
)


##############################################################################
def get_roulette_commands():
    roulette_commmands = ["!russianroulette", "!hardcoreroulette", "glockroulette",
                          "!ak47roulette", "!deathroll", "!highscores"]
    return roulette_commmands


def setup_roulette_commands(bot: commands.Bot):

    @bot.command()
    async def russianroulette(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_russian_roulette(ctx)


    @bot.command()
    async def hardcoreroulette(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_hardcore_roulette(ctx)

    
    @bot.command()
    async def glockroulette(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_glock_roulette(ctx)

    
    @bot.command()
    async def ak47roulette(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_ak47_roulette(ctx)


    @bot.command()
    async def deathroll(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_death_roll(ctx)


    @bot.command()
    async def highscores(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_highscores(ctx)
