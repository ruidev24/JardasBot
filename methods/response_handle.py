#https://raw.githubusercontent.com/Desassossego/JardasBot/refs/heads/main/methods/response_handle.py
###
import random
from discord import Message
from responses import Piropos
from responses import Generic
from responses import DarkJokes
from responses import ShowerThoughts

from database import DBquery

from utils.stopfile import validate_word
from methods import custom_handlers

#################################################
async def handle_responses(message: Message, intensity):
    try:
        roll = generate_roll(intensity)
        #refatorado
        custom_handlers.check_custom_replies(message)
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
def generate_roll(intensity: int):
    if intensity == 4:
        return 1

    max_v = round(50 / intensity)
    roll = random.randint(1, max_v)

    return roll
