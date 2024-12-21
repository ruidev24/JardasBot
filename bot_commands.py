from discord import Message
from discord.ext import commands
from methods import stats_handlers
from methods.roulette_handlers import handle_russian_roulette, handle_hardcore_roulette, handle_glock_roulette, handle_death_roll, handle_highscores
from methods.command_handlers import (
    handle_wakeup,
    handle_roast,
    handle_nuke,
    handle_defuse,
    handle_intensity,
    handle_sleep,
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
        "!vocabulary"
    ]

    return any(command in str(message.content) for command in commands) 


def setup_commands(bot: commands.Bot, allowed_mentions):
    @bot.command()
    async def acorda(ctx):
        await handle_wakeup(ctx.message)


    @bot.command()
    async def vaidormir(ctx):
        await handle_sleep(ctx.message)


    @bot.command()
    async def intensity(ctx, arg: str):
        await handle_intensity(arg)


    @bot.command()
    async def highscores(ctx):
        await handle_highscores(ctx.message)


    # Roulettes #######################################################   
    @bot.command()
    async def russianroulette(ctx):
        await handle_russian_roulette(ctx.message)


    @bot.command()
    async def hardcoreroulette(ctx):
        await handle_hardcore_roulette(ctx.message)

    
    @bot.command()
    async def glockroulette(ctx):
        await handle_glock_roulette(ctx.message)


    @bot.command()
    async def deathroll(ctx):
        await handle_death_roll(ctx.message)


    # Other ###########################################
    @bot.command()
    async def roast(ctx):
        await handle_roast(bot, ctx.message)


    @bot.command()
    async def fortuneteller(ctx):
        await handle_fortune(ctx.message)


    @bot.command()
    async def nuke(ctx):
        await handle_nuke(ctx.message, allowed_mentions)


    @bot.command()
    async def defuse(ctx):
        await handle_defuse(ctx.message)


    @bot.command()
    async def vocabulary(ctx, arg):
        await handle_vocabulary(ctx, arg)


    @bot.command()
    async def callJECS(ctx):
        await call_JECS(ctx.message)


    @bot.command()
    async def callKikaDev(ctx):
        await callKika(ctx.message)


    

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
