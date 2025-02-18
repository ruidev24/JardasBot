#https://raw.githubusercontent.com/Desassossego/JardasBot/refs/heads/main/methods/response_handle.py
###
import random
from discord import Message
from discord.ext import commands
from database import DBbotvars, DBgeneral
from methods import custom_handlers
from responses import (Piropos, Generic, DarkJokes, ShowerThoughts, BomDia, Wronged, Roasting, Thanks, Fortunes,
                       Warning, Offerings, Nuke, Huggies)


##############################################################################
async def handle_responses(message: Message):
    try:
        if await custom_handlers.check_custom_replies(message):
            return
        
        intensity = DBbotvars.get_intentsity()
        roll = generate_roll(intensity)
        if roll == 1:
            await respond_generic(message)
        return

    except Exception as e:
        print(e)



async def respond_generic(message: Message):
    # Define response categories with weights
    response_categories = [
        {"weight": 1, "response": lambda: random.choice(DarkJokes.arr_darkjokes)},   # 4% chance (1/25)
        {"weight": 1, "response": lambda: random.choice(ShowerThoughts.arr_shower)}, # 4% chance
        {"weight": 2, "response": lambda: random.choice(Piropos.arr_piropo)},        # 8% chance
        {"weight": 2, "response": lambda: random.choice(Generic.arr_low)},           # 8% chance
        {"weight": 5, "response": lambda: DBgeneral.get_strangers_vocabulary()},     # 16% chance (5/25)
        {"weight": 6, "response": lambda: random.choice(Generic.arr_medium)},        # 24% chance (6/25)
        {"weight": 8, "response": lambda: random.choice(Generic.arr_high)},          # 36% chance (8/25)
    ]

    selected_category = random.choices(response_categories, weights=[c["weight"] for c in response_categories], k=1)[0]
    
    response = selected_category["response"]()
    await message.channel.send(response)



###############################################################################################
async def respond_acordar(ctx: commands.Context):
    response = random.choice(BomDia.arr_wake)
    excluded = DBgeneral.get_least_favourable()
    if excluded:
        response += f" Excepto tu {excluded}! Tu podes ir pro caralho"
    await ctx.channel.send(response)


async def respond_sleep(ctx: commands.Context):
    response = random.choice(Wronged.arr_wronged)
    await ctx.channel.send(response)


async def respond_roast(ctx: commands.Context):
    roast = random.choice(Roasting.arr_roast)
    for mentioned_user in ctx.message.mentions:
        response = f"{mentioned_user.mention}, {roast}"
        await ctx.channel.send(response)


async def respond_self_roast(ctx: commands.Context):
    await ctx.channel.send("Querias que eu fizesse roast a mim próprio?")
    roast = random.choice(Roasting.arr_roast)
    response = f"{ctx.author.mention}, {roast}"
    await ctx.channel.send(response)


async def respond_random_roast(ctx: commands.Context):
    random_user = random.choice(ctx.guild.members) 
    roast = random.choice(Roasting.arr_roast)
    response = f"{random_user.mention}, {roast}"
    await ctx.channel.send(response)


async def respond_nuke(ctx: commands.Context):
    response = random.choice(Warning.arr_warn)
    await ctx.channel.send(response)


async def respond_defuse(ctx: commands.Context):
    response = random.choice(Thanks.arr_thanks)
    await ctx.channel.send(response)


async def respond_bomb(ctx: commands.Context):
    response = random.choice(Nuke.arr_nuke)
    await ctx.channel.send(response)


async def respond_fortune(ctx: commands.Context):
    fortune = random.choice(Fortunes.arr_fortune)
    response = f"{ctx.author.mention}, esta semana {fortune}"
    await ctx.channel.send(response)


async def respond_vocabulary(ctx: commands.Context):
    response = random.choice(Offerings.arr_offerings)
    dm = (await ctx.author.create_dm())
    await dm.send(response)


def generate_roll(intensity: int):
    if intensity == 4:
        return 1

    max_v = round(50 / intensity)
    roll = random.randint(1, max_v)

    return roll


async def respond_huggies(ctx: commands.Context):
    response = random.choice(Huggies.arr_huggies)
    await ctx.channel.send(f"{ctx.author.mention}, this is for you") 
    await ctx.channel.send(response) 
