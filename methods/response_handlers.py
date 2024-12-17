#https://raw.githubusercontent.com/Desassossego/JardasBot/refs/heads/main/methods/response_handle.py
###
import random
from discord import Message
from responses import Piropos
from responses import Generic
from responses import DarkJokes
from responses import ShowerThoughts
from responses import BomDia
from responses import Wronged
from responses import Roasting
from responses import Thanks
from responses import Fortunes
from responses import Warning
from responses import Offerings

from database import DBquery
from database import DBbotvars
from methods import custom_handlers

#################################################
async def handle_responses(message: Message):
    intensity = DBbotvars.get_intentsity()

    try:
        roll = generate_roll(intensity)
        #refatorado
        await custom_handlers.check_custom_replies(message)
        # Generic
        if roll == 1:
            await respond_generic(message)
        return

    except Exception as e:
        print(e)

#####################################################
async def respond_generic(message: Message):
    roll = random.randint(1, 21)

    if roll == 1:
        response = random.choice(DarkJokes.arr_darkjokes)
    elif roll == 2:
        response = random.choice(Piropos.arr_piropo)
    elif roll == 3:
        response = random.choice(ShowerThoughts.arr_shower)
    elif roll == 4:
        response = random.choice(Generic.arr_low)
    elif roll <= 6:
        response = DBquery.query_strangers_vocabulary()
    elif roll <= 11:
        response = random.choice(Generic.arr_medium)
    elif roll <= 21:
        response = random.choice(Generic.arr_high)
    await message.channel.send(response)


#####################################################
async def respond_acordar(message: Message):
    response = random.choice(BomDia.arr_wake)
    excluded = DBquery.query_leastFavourable()
    if excluded:
        response += f" Excepto tu {excluded}! Tu podes ir pro caralho"
    await message.channel.send(response)


async def respond_sleep(message: Message):
    response = random.choice(Wronged.arr_wronged)
    await message.channel.send(response)


async def respond_self_roast(message: Message):
    await message.channel.send("Querias que eu fizesse roast a mim próprio?")
    roast = random.choice(Roasting.arr_roast)
    response = f"{message.author.mention}, {roast}"
    await message.channel.send(response)


async def respond_roast(message: Message):
    roast = random.choice(Roasting.arr_roast)
    for mentioned_user in message.mentions:
        response = f"{mentioned_user.mention}, {roast}"
        await message.channel.send(response)


async def respond_defuse(message: Message):
    response = random.choice(Thanks.arr_thanks)
    await message.channel.send(response)

async def respond_nuke(message):
    response = random.choice(Warning.arr_warn)
    await message.channel.send(response)


async def respond_fortune(message:Message):
    fortune = random.choice(Fortunes.arr_fortune)
    response = f"{message.author.mention}, esta semana {fortune}"
    await message.channel.send(response)


async def respond_vocabulary(ctx):
    response = random.choice(Offerings.arr_offerings)
    dm = (
        await ctx.author.create_dm()
    )  # If dm is already made, it does not matter :)
    await dm.send(response)

#####################################################
def generate_roll(intensity: int):
    if intensity == 4:
        return 1

    max_v = round(50 / intensity)
    roll = random.randint(1, max_v)

    return roll
