import discord
import logging
import logging.handlers
from discord.errors import DiscordException
import random
from discord.ext import commands
import time
from methods.response_handle import handle_responses
from utils.utils import check_for_cheats, respond_mention
from database import DBupdate

from methods import stats_handle
from methods.logging_handle import setup_logging
from methods.command_handle import (
    wakeup,
    self_roast,
    handle_roast,
    respond_nuke,
    respond_defuse,
    change_intensity,
    handle_fortune,
    russian_roulette,
    glock_roulette,
    call_JECS,
    callKika
)
from responses import Offerings

from utils.state import STATE

state = STATE.NORMAL
div_intensity = 3
message_count = 0
timestamp = None


########################################################
def run_discord_bot():
    global state
    global div_intensity

    #log_handler
    logger = logging.getLogger('discord')
    setup_logging(logger)

    # Discord Code - Ainda nao vi a documentaçao
    TOKEN = ""
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)
    allowed_mentions = discord.AllowedMentions(everyone=True)

    # Events
    @bot.event
    async def on_ready():
        print(f"{bot.user} is running!")

    # On Message
    @bot.event
    async def on_message(message: discord.Message):
        try:
            await bot.process_commands(message)
        except [TypeError, DiscordException]:
            print("OK")
        # Aqui devia dar return se processou algum comando

        try:
            global state
            global div_intensity

            # ignore messages by bot
            if message.author == bot.user:
                await dont_let_spam(message)
                return

            # FOR DEBUG
            # if str(message.author) != "ruimachado":
            #     return

            # Update stats
            # stats_handle.update_stats(message)

            # Sleeping
            if state == STATE.SLEEP:
                return

            # Check Cheats
            if await check_for_cheats(message):
                return

            # Mention the Bot
            if bot.user.mentioned_in(message):
                await respond_mention(message)
                return

            await handle_responses(message, div_intensity)

        except Exception as e:
            print(e)

    # Commands

    @bot.command()
    async def callJECS(ctx):
        await call_JECS(ctx.message)

    @bot.command()
    async def callKikaDev(ctx):
        await callKika(ctx.message)

    @bot.command()
    async def glockroulette(ctx):
        await glock_roulette(ctx.message)

    @bot.command()
    async def fortune_teller(ctx):
        await handle_fortune(ctx.message)

    @bot.command()
    async def russianroulette(ctx):
        await russian_roulette(ctx.message)

    @bot.command()
    async def acorda(ctx):
        global state
        await wakeup(ctx.message, state)
        state = STATE.NORMAL

    @bot.command()
    async def vaidormir(message: discord.Message):
        global state
        await vaidormir(message)
        state = STATE.SLEEP

    @bot.command()
    async def nuke(message: discord.Message):
        await respond_nuke(message, allowed_mentions)

    @bot.command()
    async def defuse(message: discord.Message):
        await respond_defuse(message)

    @bot.command()
    async def intensity(_: discord.Message, arg: str):
        global div_intensity
        div_intensity = await change_intensity(arg)

    @bot.command()
    async def roast(ctx):
        mentioned_users = ctx.message.mentions
        if bot.user.mentioned_in(ctx.message):
            await ctx.channel.send("Querias que eu fizesse roast a mim próprio?")
            await self_roast(ctx.message)
            return
        if mentioned_users:
            await handle_roast(ctx.message)
        else:
            await ctx.channel.send("Dou roast a quem? Seu burro!")

    @bot.command()
    async def vocabulary(ctx, arg):
        DBupdate.update_vocabulary(arg, str(ctx.author))
        response = random.choice(Offerings.arr_offerings)
        dm = (
            await ctx.author.create_dm()
        )  # If dm is already made, it does not matter :)
        await dm.send(response)

    # Commands Stats
    @bot.command()
    async def stats(message: discord.Message):
        stats_handle.get_top_words_general(message)

    @bot.command()
    async def stats_user(message: discord.Message):
        stats_handle.get_top_words_by_user(message)

    @bot.command()
    async def stats_word(message: discord.Message):
        stats_handle.get_top_users_by_word(message)

    @bot.command()
    async def stats_channel(message: discord.Message):
        stats_handle.get_top_words_by_channel(message)

    #################
    bot.run(TOKEN, log_handler=None)

####################################################################
async def dont_let_spam(message: discord.Message):
    global timestamp
    global message_count
    global div_intensity
    # Update message count and timestamp
    current_time = time.time()

    if timestamp is None:
        message_count = 0
        timestamp = current_time

    message_count += 1

    # Check if message count exceeds the limit
    if message_count > 10:
        if current_time - timestamp < 60:
            # Stop spamming
            await message.channel.send(
                "Vou-me calar que o caralho do meu pai não quer que eu seja spammer"
            )
            div_intensity = 1
            time.sleep(180)
            await message.channel.send("Voltei caralho")

        message_count = 0
        timestamp = current_time


#################################################################################3
if __name__ == "__main__":
    run_discord_bot()
