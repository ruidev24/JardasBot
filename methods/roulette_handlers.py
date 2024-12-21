import random
from datetime import timedelta
from discord import Message
from database import DBbotvars
from database import DBroulette



async def handle_russian_roulette(message: Message):
    bullet = random.randint(1, 6)
    DBroulette.update_russian_score(message.author)

    if bullet == 1:
        DBroulette.reset_russian_curr_score(message.author)
        try:
            
            timeout_duration = timedelta(hours=1)
            await message.author.timeout(timeout_duration, reason="Drawn the bullet in Russian Roulette")
            await message.channel.send(f"{message.author.mention} has died")
        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")
    else:
        await message.channel.send(f"{message.author.mention} is safe!")


async def handle_hardcore_roulette(message: Message):
    rand = random.randint(1,100)
    if rand == 1:
        timeout_duration = timedelta(hours=24)
    elif rand <= 6:
        timeout_duration = timedelta(hours=6)
    elif rand <= 16:
        timeout_duration = timedelta(hours=3)
    elif rand <= 36:
        timeout_duration = timedelta(hours=2)
    elif rand <= 50:
        timeout_duration = timedelta(hours=1)
    elif rand <= 64:
        timeout_duration = timedelta(minutes=45)
    elif rand <= 84:
        timeout_duration = timedelta(minutes=30)
    elif rand <= 94:
        timeout_duration = timedelta(minutes=10)
    elif rand <= 99:
        timeout_duration = timedelta(minutes=5)
    elif rand == 100:
        timeout_duration = timedelta(minutes=1)

    bullet = random.randint(1, 3)
    DBroulette.update_hardcore_score(message.author)
    if bullet == 1:
        DBroulette.reset_hardcore_curr_score(message.author)
        try:
            await message.author.timeout(timeout_duration, reason="Drawn the bullet in Hardcore Roulette")
            await message.channel.send(f"{message.author.mention} has died")
        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")
    else:
        await message.channel.send(f"{message.author.mention} is safe!")


async def handle_glock_roulette(message: Message):
    bullet = random.randint(1, 99)
    DBroulette.update_glock_score(message.author)
    if bullet != 1:
        DBroulette.reset_glock_curr_score(message.author)
        try:
            timeout_duration = timedelta(minutes=10)
            await message.author.timeout(timeout_duration, reason="Drawn the bullet with a gun.")
            await message.channel.send(f"{message.author.mention} has died")
        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")
    else:
        await message.channel.send(f"{message.author.mention} is safe! The gun jammed.")





async def handle_death_roll(message: Message):
    old_death_roll = DBbotvars.get_death_roll()
    curr_death_roll = random.randint(1, old_death_roll)
    await message.channel.send(f"Deathroll = {curr_death_roll}")

    if curr_death_roll == 1:
        try:
            timeout_duration = timedelta(hours=3)
            await message.author.timeout(timeout_duration, reason="Drawn the bullet in Deathroll")
            await message.channel.send(f"{message.author.mention} has died")
            DBbotvars.update_death_roll(100)

        except Exception as e:
            await message.channel.send(f"Error timing out {message.author.mention}: {e}")
    else:
        await message.channel.send(f"{message.author.mention} is safe!")
        DBbotvars.update_death_roll(curr_death_roll)


# TODO
async def handle_highscores(message: Message):
    message_txt = "" 
    
    message_txt += "\nRussian Roulette LeaderBoard\n"
    champions_russian = DBroulette.get_highscores_russian()
    pos = 0
    for champ in champions_russian:
        pos += 1
        message_txt += f"Number {pos}: {champ[1]} - {champ[0]}\n"

    message_txt += "\nHardcore Roulette LeaderBoard\n"
    champions_hardcore = DBroulette.get_highscores_hardcore()
    pos = 0
    for champ in champions_hardcore:
        pos += 1
        message_txt += f"Number {pos}: {champ[1]} - {champ[0]}\n"

    message_txt += "\nGlock Roulette LeaderBoard\n"
    champions_glock = DBroulette.get_highscores_glock()
    pos = 0
    for champ in champions_glock:
        pos += 1
        message_txt += f"Number {pos}: {champ[1]} - {champ[0]}\n"

    await message.channel.send(message_txt)
