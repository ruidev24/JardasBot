import random
import tabulate
from responses import BomDia
from discord.ext import commands
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database import DBgeneral, DBnuke, DBstatistics


##############################################################################
def handle_schedules(bot: commands.Bot):
    daily_0am = CronTrigger(hour=0, minute=00)
    daily_8am = CronTrigger(hour=8, minute=00)
    weekly = CronTrigger(day_of_week="mon", hour=1, minute=00)
    monthly = CronTrigger(day=1, hour=13, minute=00)
    friday_13th = CronTrigger(day=13, day_of_week="fri", hour=0, minute=00)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(lambda: bot.loop.create_task(sched_remind_events(bot)), CronTrigger(day_of_week="wed-sat", hour=10, minute=00))

    scheduler.add_job(lambda: bot.loop.create_task(sched_nuke_reset(bot)), daily_0am)
    scheduler.add_job(lambda: bot.loop.create_task(sched_mention_reset(bot)), daily_0am)
    scheduler.add_job(lambda: bot.loop.create_task(sched_bom_dia(bot)), daily_8am)

    scheduler.add_job(lambda: bot.loop.create_task(sched_fortune_reset(bot)), weekly)
    scheduler.add_job(lambda: bot.loop.create_task(sched_stats_monthly(bot)), monthly)

    scheduler.start()


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


async def sched_fortune_reset(bot: commands.Bot):
    DBgeneral.reset_fortune_table()


async def sched_mention_reset(bot: commands.Bot):
    DBgeneral.reset_mention_table()


async def sched_nuke_reset(bot: commands.Bot):
    DBnuke.reset_nuke_table()


async def sched_stats_monthly(bot: commands.Bot):
    channel1 = bot.get_channel(1103037425690882139) # channel - taberna
    top_words = DBstatistics.get_words()
    
    table = tabulate(top_words, headers=["Word", "Count"], tablefmt="simple_outline")
    await channel1.send(f"The most used words in this discord server are:\n```\n{table}\n```")