import random
from discord import Message
from utils.stopfile import validate_word
from responses import Custom


##############################################################################
async def check_custom_replies(message: Message):
    if await caralhamos(message):
        return True
    if (str(message.author) == "curlyfry591") and await custom_reply(message, Custom.arr_german):
        return True
    if (str(message.author) == "shipyroni") and await custom_reply(message, Custom.arr_latin):
        return True
    if (str(message.author) == "carosaf") and await custom_reply(message, Custom.arr_french):
        return True
    if (str(message.author) == "jecs21") and await custom_reply(message, Custom.arr_communism):
        return True
    if (str(message.author) == "lazersword996") and await custom_reply(message, Custom.arr_japanese):
        return True
    if (str(message.author) == "toirao") and await custom_reply(message, Custom.arr_euskara):
        return True
    if str(message.author) == "rebolamercedes" and "@everyone" in message.content:
        await rebola_is_conas(message)
        return True
    return False


async def rebola_is_conas(message: Message):
    message.channel.send(message, "oh caralho e parares com essa merda?")
    message.channel.send(message, "És estupido ou que?")
    message.channel.send(message, "Deves ter batido com a cabeça em miudo só pode")
    message.channel.send(message, "Caralho do moço")


async def custom_reply(message: Message, custom_dict: Custom):
    roll = random.randint(1, 20)
    if roll == 1:
        response = random.choice(custom_dict)
        await message.channel.send(response)
        return True
    return False


async def caralhamos(message: Message):
    caralhamos_roll = random.randint(1, 100)
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
