import random

from responses import Generic
from responses import DarkJokes
from responses import ShowerThoughts
from responses import Roasting
from responses import German
from responses import Piropos

from DataBase import DBupdate

from utils.stopfile import *
from utils.utils import *                                                                                                                                                                                                                                                                                                                       


#################################################
async def handle_Responses(message, intensity):
    try:
        roll = generate_roll(intensity)
        p_message = message.content.lower()

        # Caralhamos
        if await caralhamos(message):
            return

        # Check if curlyfry
        if(str(message.author) == "curlyfry591") and await german_reply(message):
            return
        
        # Check if Rebola is Conas
        elif(str(message.author) == "rebolamercedes" and "@everyone" in message.content):
            await rebola_is_conas(message)

        # Generic
        if roll == 1:
            await respond_generic(message)

        return

    except Exception as e:
        print(e)   


###########################################################################
async def rebola_is_conas(message):
    message.channel.send(message, "oh caralho e parares com essa merda?")
    message.channel.send(message, "És estupido ou que?")
    message.channel.send(message, "Deves ter batido com a cabeça em miudo só pode")
    message.channel.send(message, "Caralho do moço")


######################################################
async def german_reply(message):
    roll = random.randint(1,30)
    if roll == 1:
        response = random.choice(German.arr_german)
        await message.channel.send(response)
        return True
    return False


#####################################################
async def respond_generic(message):
    roll = random.randint(1,21)

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


######################################################
async def caralhamos(message):
    caralhamos_roll = random.randint(1,100)
    message_text = str(message.content).lower()
    words = message_text.split()

    if caralhamos_roll != 1:
        return False
    
    for word in words:
        if not validate_word(word):
            continue

        if len(word) <= 4:
            continue

        if word.endswith("ar") or word.endswith("er"):
            await message.channel.send(word[:-1] + "mos")
            return True

        if word.endswith("ir"):
            await message.channel.send(word[:-2] + "emos")
            return True
        
        if word.endswith("o") and not word.endswith("ao"):
            await message.channel.send(word[:-1] + "amos")
            return True
        
        if word.endswith("a"):
            await message.channel.send(word + "mos")
            return True
        
    return False


#####################################################
def generate_roll(intensity):
    max_v = round(50 / intensity)
    roll = random.randint(1, max_v)

    if intensity == 4:
        roll = 1

    return roll
