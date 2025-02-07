from discord.ext import commands
from datetime import timedelta

from methods.response_handlers import (
    respond_huggies
)


##############################################################################
async def handle_huggies(ctx: commands.Context):
    await respond_huggies(ctx)


async def handle_mistery(ctx: commands.Context):
    await ctx.channel.send("Mistery command has been activated")


async def handle_sacrifice(ctx: commands.Context):        
    for mentioned_user in ctx.message.mentions:
        try:
            if str(mentioned_user) == 'ruimachado':
                await ctx.channel.send("Get Shrekt Nerds")
                return

            timeout_duration = timedelta(minutes=1)
            await mentioned_user.timeout(timeout_duration, reason="Sacrificed to Khali")
            await ctx.channel.send(f"{mentioned_user.mention} has been sacrificed")
        except Exception as e:
            await ctx.channel.send(f"Error timing out {mentioned_user.mention}: {e}")


async def handle_shrekt(ctx: commands.Context):
    if str(ctx.author) != "ruimachado":
        await ctx.channel.send("Get Shrekt nerds!")
        return

    for mentioned_user in ctx.message.mentions:
        await mentioned_user.edit(nick="O Rui é o melhor mod")

async def handle_super_shrekt(ctx: commands.Context, arg: str):
    for mentioned_user in ctx.message.mentions:
        try:
            if str(mentioned_user) == 'ruimachado':
                await ctx.channel.send("Get Shrekt Nerds")
                return

            await mentioned_user.edit(nick=arg)
        except Exception as e:
            await ctx.channel.send(f"Error {mentioned_user.mention}: {e}")



async def handle_list_events(ctx: commands.Context):
    """List all scheduled events in the guild."""
    events = await ctx.guild.fetch_scheduled_events()
    if not events:
        await ctx.send("No events are currently scheduled.")
    else:
        for event in events:
            if(str(event.name) == "Convívio semanal 🍻"):
                await ctx.send(f"{event.name} - {event.start_time} {event.status}")
                await(ctx.send(event.url))

            # print(event._users)
            # print(event.__repr__)
            # await ctx.send(f"{event.name} - {event.start_time} {event.status}")
            # await(ctx.send(event.url))

            # subscribers = await event.fetch_subscribers()
            # for user in subscribers:
            #     print(user)


#################################################################
async def call_JECS(ctx: commands.Context):
    if str(ctx.author) == "leomarcuzzo":
        try:
            await ctx.channel.send("<@192306440315076608> anda cá.")
            await ctx.channel.send("<@192306440315076608> anda cá.")
            await ctx.channel.send("<@192306440315076608> anda cá.")
        except Exception as e:
            await ctx.channel.send("Error sending message: {e}")
    else:
        pass

    

async def callKika(ctx: commands.Context):
    if str(ctx.author) == "leomarcuzzo":
        try:
            await ctx.channel.send("<@402215966169235466> desenvolva-me.")
        except Exception as e:
            await ctx.channel.send("Error sending message: {e}")
    else:
        pass
