import discord
import logging
import logging.handlers
from discord import Message
from discord.errors import DiscordException
from discord.ext import commands

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot_commands import setup_commands, is_command
from methods.logging_handlers import setup_logging
from methods.response_handlers import handle_responses
from methods.stats_handlers import update_stats
from methods.schedule_events_handler import remind_events
from database.DBbotvars import get_state
from utils.utils import check_for_cheats, handle_mention
from utils.state import STATE



async def process_commands(bot: commands.Bot, message: Message):
    try:
        await bot.process_commands(message)
        return is_command(message)
    except [TypeError, DiscordException]:
        print("Command Error")


async def process_message(bot: commands.Bot, message: Message):
    try:
        if STATE(get_state()) == STATE.SLEEP: return
        
        if message.author == bot.user:
            return
                 
        if await check_for_cheats(message):
            return

        # Mention Bot
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
    TOKEN = ''
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

        # Initialize the scheduler
        scheduler = AsyncIOScheduler()
        scheduler.add_job(lambda: bot.loop.create_task(remind_events(bot)), CronTrigger(day_of_week="wed-sat", hour=10, minute=00))
        scheduler.start()

    @bot.event
    async def on_message(message: discord.Message):
        #await update_stats(message)
        is_command = await process_commands(bot, message)

        if not is_command:
            await process_message(bot, message)


    bot.run(TOKEN, log_handler=None)



############################################################
############################################################
if __name__ == "__main__":
    run_discord_bot()