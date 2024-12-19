import discord
import logging
import logging.handlers
from discord import Message
from discord.errors import DiscordException
from discord.ext import commands

from bot_commands import setup_commands
from methods.logging_handlers import setup_logging
from methods.response_handlers import handle_responses
from database.DBbotvars import get_state
from utils.utils import check_for_cheats, respond_mention
from utils.state import STATE


async def process_commands(bot: commands.Bot, message: Message):
    try:
        await bot.process_commands(message)
    except [TypeError, DiscordException]:
        print("Command Error")


async def process_message(bot: commands.Bot, message: Message):
    try:
        if str(message.author) != "ruimachado":
            return

        if message.author == bot.user:
            return
        
        # Sleeping
        state = get_state()
        print (f"debug = {state}")
        if state == STATE.SLEEP:
            return

        # Check Cheats
        if await check_for_cheats(message):
            return

        # Mention Bot
        if bot.user.mentioned_in(message):
            await respond_mention(message)
            return

        await handle_responses(message)

    except Exception as e:
        print(e)


def run_discord_bot():
    # log_handler
    logger = logging.getLogger('discord')
    setup_logging(logger)

    # Discord Code - Still exploring documentation
    TOKEN = ''
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    allowed_mentions = discord.AllowedMentions(everyone=True)
    setup_commands(bot, allowed_mentions)

    ###############################################
    @bot.event
    async def on_ready():
        print(f"{bot.user} is running!")

    @bot.event
    async def on_message(message: discord.Message):
        await process_commands(bot, message)
        await process_message(bot, message)

    bot.run(TOKEN, log_handler=None)



############################################################
############################################################
if __name__ == "__main__":
    run_discord_bot()