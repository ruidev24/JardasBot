import discord
from discord.ext import commands
import asyncio
import time

import Zresponse_Handle as Zresponse_Handle
import utils.stopwords as stopwords
import DataBase.DBupdate as DBupdate
import DataBase.DBquery as DBquery

from utils.state import STATE


global state
global intensity
global mention_cnt

global message_count
global timestamp


def run_discord_bot():
    # Discord Code - Ainda nao vi a documentaçao
    TOKEN = ''
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents = intents)
    
    global state
    global intensity
    global mention_cnt
    state = STATE.NORMAL
    mention_cnt = 0
    intensity = 4

    global message_count
    global timestamp
    message_count = 0
    timestamp = None



    @client.event
    async def on_ready():
        print(f'{client.user} is running!')
        # Get the guild object
        guild = client.guilds[0]  # Assuming your bot is in only one guild
        # await get_history_all_channels(guild)


    @client.event
    async def on_message(message):
        try:
            global state
            global intensity

            # ignore messages by bot
            if message.author == client.user:
                await dont_let_spam(message)
            
            # FOR DEBUG
            if str(message.author) != "ruimachado":
                return
            
            # Update stats
            update_stats(message)

            # Check Wake up
            if message.content == "!acorda":
                wakeup(message)

            # Sleeping
            if state == STATE.SLEEP:
                return

            # Check Cheats
            checkForCheats(message)

            # Change intensity
            if "!intensity=" in message.content:
                change_intensity(message)
                return

            # Mention the Bot
            if client.user.mentioned_in(message):
                await respond_mention(message)  

            # Respond
            if state != STATE.SLEEP:
                state = await Zresponse_Handle.handle_Responses(message, state, intensity)

        except Exception as e:
            print(e)

    #################
    client.run(TOKEN)


####################################################################
async def dont_let_spam(message):
    global timestamp
    global message_count
    global intensity
    # Update message count and timestamp
    current_time = time.time()

    if timestamp is None:
        message_count = 0
        timestamp = current_time

    message_count += 1

    # Check if message count exceeds the limit
    if message_count > 20:
        if current_time - timestamp < 30:
            # Stop spamming
            await message.channel.send("Vou-me calar que o caralho do meu pai não quer que eu seja spammer")
            intensity = 1
            time.sleep(180)
            await message.channel.send("Voltei caralho")
            
        message_count = 0
        timestamp = current_time


####################################################################
async def wakeup(message):
    global state
    if state == STATE.SLEEP:
        state = STATE.WAKE
    else:
        await message.channel.send("Já tou acordado caralho, cala-te")
        return


##########################################
async def respond_mention(message):
    DBupdate.update_mention_cnt(str(message.author))
    mention_cnt = DBquery.query_mention_count(str(message.author))

    if int(mention_cnt) < 10:
        await Zresponse_Handle.respond_mention_general(message)
        return
    elif int(mention_cnt) == 10:
        await message.channel.send("Ai queres festa? Já te fodo")
        return
    else:
        await Zresponse_Handle.respond_mention_dm(message)
        return


#####################################################
async def get_history_all_channels(guild):
    try:
        # Iterate over every channel in the server
        for channel in guild.channels:
            # Check if the channel is a text channel
            if isinstance(channel, discord.TextChannel):
                await get_history(channel)  # Await the execution of asynchronous function
    except Exception as e:
        print("Error:", e)


##################################################
async def get_history(channel):
    try:
        async for message in channel.history():
            update_stats(message)
    except Exception as e:
        print("Error:", e)


#####################################################
def update_stats(message):
    username = str(message.author) 
    message_text = str(message.content).lower()
    channel = str(message.channel)

    DBupdate.update_users(message)
    DBupdate.update_channels(message)

    words = message_text.split()

    for word in words:
        if not stopwords.validate_word(word):
            continue
        DBupdate.update_words(word)
        DBupdate.update_user_words(username, word)
        DBupdate.update_channel_words(channel, word)


#################################################
def checkForCheats(message): 
    global state

    try:    
        message_text = str(message.content).lower()
        words = message_text.split() 
    
        stats = {}
        for word in words:
            if word in stats:
                stats[word] += 1
            else:
                stats[word] = 1

            if stats[word] > 10:
                state = STATE.CHEAT
    except Exception as e:
        print("Error checking for cheats:", e)
    

#################################################
def change_intensity(message):
    global intensity 

    value = int(message.content[11])
    if value >= 1 and value <= 4:
        intensity = value


#################################################################################3
if __name__ == '__main__':
    run_discord_bot()
