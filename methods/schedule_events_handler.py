import random
from responses import BomDia
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database import DBgeneral

def handle_schedules(bot: commands.Bot):
    # Initialize the scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: bot.loop.create_task(sched_remind_events(bot)), CronTrigger(day_of_week="wed-sat", hour=10, minute=00))
    scheduler.add_job(lambda: bot.loop.create_task(sched_bom_dia(bot)), CronTrigger(hour=8, minute=00))
    scheduler.start()

async def sched_test(bot: commands.Bot):
    channel1 = bot.get_channel(1103037425690882139) # channel - taberna
    await channel1.send("Test Caralho")


async def sched_remind_events(bot: commands.Bot):
    guild = bot.get_guild(1103037425099481192)      # guild - biocenose
    channel1 = bot.get_channel(1103037425690882139) # channel - taberna
    channel2 = bot.get_channel(1103059671260086463) # channel - convivios

    events = await guild.fetch_scheduled_events()
    for event in events:
        event_start_utc = event.start_time.astimezone(timezone.utc)
        today_utc = datetime.now(timezone.utc)
        if (event.name == "Convívio semanal 🍻") and ( (event_start_utc - today_utc) < timedelta(days=7) ):
            await channel1.send(f"Este sábado há convívios, apareçam seus caralhos")
            await channel1.send(event.url)
            await channel2.send(f"Este sábado há convívios, apareçam seus caralhos")
            await channel2.send(event.url)


async def sched_bom_dia(bot: commands.Bot):
    channel1 = bot.get_channel(1103037425690882139) # channel - taberna
    response = random.choice(BomDia.arr_wake)
    await channel1.send(response)


async def sched_fortune_reset(bot: commands):
    DBgeneral.reset_fortune()