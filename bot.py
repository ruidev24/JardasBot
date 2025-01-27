import discord
import os
from dotenv import load_dotenv
import logging
import logging.handlers
from discord import Message
from discord.errors import DiscordException
from discord.ext import commands

from commands.handle_bot_commands import setup_commands, is_command
from methods.logging_handlers import setup_logging
from methods.response_handlers import handle_responses
from methods.schedule_events_handler import handle_schedules
from utils.utils import check_for_cheats, handle_mention
from database.DBbotvars import bot_is_sleeping


load_dotenv()

async def process_commands(bot: commands.Bot, message: Message):
    try:
        await bot.process_commands(message)
        return is_command(message)
    except [TypeError, DiscordException]:
        print("Command Error")


async def process_message(bot: commands.Bot, message: Message):
    try:
        if bot_is_sleeping(): return
        if message.author == bot.user: return
        if await check_for_cheats(message): return
            
        if bot.user.mentioned_in(message):
            await handle_mention(message)
            return

        await handle_responses(message)

    except Exception as e:
        print(e)




def run_discord_bot():
    # log_handler
    logger = logging.getLogger('discord')
    setup_logging(logger)

    # Discord Code - Still exploring documentation
    TOKEN = os.getenv("TOKEN")
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    # allowed_mentions = discord.AllowedMentions(everyone=True)
    setup_commands(bot)

    ###############################################
    @bot.event
    async def on_ready():
        print(f"{bot.user} is running!")
        handle_schedules(bot)


    @bot.event
    async def on_message(message: discord.Message):
        #await update_stats(message)
        is_command = await process_commands(bot, message)

        if not is_command:
            await process_message(bot, message)


    @bot.event
    async def on_member_join(member):
        query_insert = """INSERT INTO users (username, nick) VALUES (?,?)"""
        # db_execute(query_insert, (str(member), str(member.server_nick)))

    bot.run(TOKEN, log_handler=None)



############################################################
############################################################
if __name__ == "__main__":
    run_discord_bot()