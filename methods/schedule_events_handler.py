from discord.ext import commands
from datetime import datetime, timedelta, timezone

async def remind_events(bot: commands.Bot):
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
