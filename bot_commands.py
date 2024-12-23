from discord import Message
from discord.ext import commands
from methods import stats_handlers
from database.DBbotvars import get_state
from utils.state import STATE
from methods.roulette_handlers import handle_russian_roulette, handle_hardcore_roulette, handle_glock_roulette, handle_ak47_roulette, handle_death_roll, handle_highscores
from methods.nuke_handlers import handle_nuke, handle_defuse, store_nicks
from methods.command_handlers import (
    handle_wakeup,
    handle_sleep,
    handle_intensity,
    handle_mistery,
    handle_status,
    handle_huggies,
    
    handle_roast,
    handle_fortune, 
    handle_vocabulary,

    call_JECS,
    callKika
)


def is_command(message: Message):
    commands = [
        "!acorda", "!vaidormir", "!intensity", "!highscores",
        "!russianroulette", "!hardcoreroulette", "!glockroulette",
        "!deathroll", "!roast", "!fortuneteller", "!nuke", "!defuse",
        "!vocabulary", "!mistery", "!ak47roulette"
    ]
    return any(command in str(message.content) for command in commands) 


def setup_commands(bot: commands.Bot):
    # Base #########################################################
    @bot.command()
    async def acorda(ctx: commands.Context):
        await handle_wakeup(ctx)


    @bot.command()
    async def vaidormir(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_sleep(ctx)


    @bot.command()
    async def intensity(ctx: commands.Context, arg: str):
        if STATE(get_state()) == STATE.SLEEP: return
        await handle_intensity(arg)


    @bot.command()
    async def status(ctx: commands.Context):
        await handle_status(ctx)

    
    @bot.command()
    async def mistery(ctx: commands.Context):
        await store_nicks(ctx)
        await handle_mistery(ctx)


    @bot.command()
    async def huggies(ctx: commands.Context):
        await handle_huggies(ctx)


    # Roulettes #######################################################   
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


    @bot.command()
    async def callJECS(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await call_JECS(ctx)


    @bot.command()
    async def callKikaDev(ctx: commands.Context):
        if STATE(get_state()) == STATE.SLEEP: return
        await callKika(ctx)


    # Stats ###################################################
    @bot.command()
    async def stats(ctx):
        await stats_handlers.get_top_words_general(ctx.message)


    @bot.command()
    async def stats_user(ctx):
        await stats_handlers.get_top_words_by_user(ctx.message)


    @bot.command()
    async def stats_word(ctx):
        await stats_handlers.get_top_users_by_word(ctx.message)


    @bot.command()
    async def stats_channel(ctx):
        await stats_handlers.get_top_words_by_channel(ctx.message)
