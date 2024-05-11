import random
import datetime
import sqlite3
import time

import responses.Generic as Generic
import responses.Wronged as Wronged
import responses.BomDia as BomDia
import responses.Cheats as Cheats
import responses.Mentions as Mentions
import responses.Warning as Warning
import responses.Thanks as Thanks
import responses.Roasting as Roasting
import responses.German as German

import DataBase.DBdelete as DBdelete
import DataBase.DBupdate as DBupdate
import DataBase.DBquery as DBquery

from utils.state import STATE


#############################################################################
async def send_message(message, response):
    try:
        await message.channel.send(response)
    except Exception as e:
        print(e)                                                                                                                                                                                                                                                                                                                              


######################################################
async def handle_roast(message):
    roast = random.choice(Roasting.arr_roast)
    mentioned_user = message.mentions[0]
    response = f"{mentioned_user.mention}, {roast}"
    await send_message(message, response)


######################################################
async def german_reply(message):
    roll = random.randint(1,30)
    if roll == 1:
        response = random.choice(German.arr_german)
        await send_message(message, response)
        return True
    return False


#################################################
async def handle_Responses(message, state, intensity):
    try:
        roll = generate_roll(intensity)
        p_message = message.content.lower()

        # Check if Rebola is Conas
        if(str(message.author) == "rebolamercedes" and "@everyone" in message.content):
            await rebola_is_conas(message)
            return state
        
        # Check if curlyfry
        if(str(message.author) == "curlyfry591"):
            msg = await german_reply(message)
            if msg:
                return state
        
        # Check if Cheats
        if state == STATE.CHEAT:
            await respond_cheats(message)
            return STATE.NORMAL
        
        # Check Acordar
        if state == STATE.WAKE:
            await respond_acordar(message)
            return STATE.NORMAL
        
        # Check Vai Dormir
        if p_message == "!vaidormir":
            await respond_dormir(message)
            return STATE.SLEEP
        
        # Check if Nuke
        if p_message == "!nuke":
            await respond_nuke(message)
            return state

        # Check if Defuse
        if p_message == "!4,8,15,16,23,42":
            await respond_defuse(message)
            return state

        # Check if Roast
        if "!roast=" in message.content and len(message.mentions) > 0:
            await handle_roast(message)
            await handle_roast(message)

        # Check if Vocabulary
        if "!vocabulario=" in message.content:
            await handle_vocabulary(message)

        # Generic
        if roll == 1:
            await respond_generic(message)
            return state
        
        # elif p_message == "!stats":
        #     get_top_words_general(message)
        # elif "!stats!user=" in p_message:
        #     get_top_words_by_user(message)
        # elif "!stats!word=" in p_message:
        #     get_top_users_by_word(message)
        # elif "!stats!channel=" in p_message:
        #     get_top_words_by_channel(message)

        return state

    except Exception as e:
        print(e)   


#####################################################
async def handle_vocabulary(message):
    vocabulary = message.content.split("=")[1]
    username = message.author
    DBupdate.update_vocabulary


###########################################################################
async def rebola_is_conas(message):
    send_message(message, "oh caralho e parares com essa merda?")
    send_message(message, "És estupido ou que?")
    send_message(message, "Deves ter batido com a cabeça em miudo só pode")
    send_message(message, "Caralho do moço")


#####################################################
async def respond_cheats(message):
    response = random.choice(Cheats.arr_cheats)
    await send_message(message, response)


####################################################
async def respond_acordar(message):
    response = random.choice(BomDia.arr_wake)
    excluded = DBquery.query_leastFavourable()
    DBupdate.update_positiveFavour(str(message.author))
    if(excluded):
        response += f" Excepto tu {excluded}! Tu podes ir pro caralho"
    await send_message(message, response)


####################################################
async def respond_mention_dm(message):
    response = random.choice(Mentions.arr_mention)
    dm = await message.author.create_dm() #If dm is already made, it does not matter :)
    await dm.send(response)


####################################################
async def respond_mention_general(message):
    response = random.choice(Mentions.arr_mention)
    await message.channel.send(response)


######################################################
async def respond_dormir(message):
    DBupdate.update_negativeFavour(str(message.author))
    response = random.choice(Wronged.arr_wronged)
    await send_message(message, response)


#####################################################
async def respond_nuke(message):
    today = datetime.date.today()
    last_date = DBquery.query_nuke_last_date()
    if str(last_date) != str(today):
        print("YO")
        DBdelete.clear_nuke_table()

    prev_cnt = DBquery.query_nuke_count()
    DBupdate.update_nuke_count(str(message.author))
    counter = DBquery.query_nuke_count()

    if counter == prev_cnt:
        await send_message(message, "Não há repeats")
        return

    if counter < 10:
        response = random.choice(Warning.arr_warn)
        await send_message(message, response)
    else:
        await nuke_channel(message)


#####################################################
async def respond_defuse(message):
    prev_cnt = DBquery.query_nuke_count()
    DBupdate.update_defuse_count(str(message.author))
    counter = DBquery.query_nuke_count()

    if counter == prev_cnt:
        await send_message(message, "Não há repeats")
        return
    
    response = random.choice(Thanks.arr_thanks)
    await send_message(message, response)


#####################################################
async def respond_generic(message):
    roll = random.randint(1,15)
    if roll == 1:
        response = random.choice(Generic.arr_low)
    if roll <= 2:
        response = random.choice(Generic.arr_low)
    elif roll <= 5:
        response = random.choice(Generic.arr_medium)
    elif roll <= 15:
        response = random.choice(Generic.arr_high)
    await send_message(message, response)


#####################################################
async def nuke_channel(message):
    await send_message(message, "Nuke activated...")
    await send_message(message, "NOW I AM BECOME DEATH, THE DESTROYER OF WORLDS...")
    time.sleep(60)
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")
    await send_message(message, "@everyone")


#####################################################
def generate_roll(intensity):
    max_v = round(50 / intensity)
    roll = random.randint(1, max_v)

    if intensity == 4:
        roll = 1

    return roll


##################################################
async def get_top_users_by_word(message):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        word = message.content[12:]
        word = word.lower()
        word = word.replace(" ","")
        print(word)

        # Check if the word exists
        c.execute("SELECT word FROM words WHERE word = ?", (word,))
        word_id = c.fetchone()
        if not word_id:
            return "That words has never been written"

        # Query to get the top 10 words by user
        c.execute("""
            SELECT u.username, uw.count
            FROM userwords uw
            JOIN words w ON uw.word_id = w.word_id
            JOIN users u ON uw.user_id = u.user_id
            WHERE w.word = ?
            ORDER BY uw.count DESC
            LIMIT 10
        """, (word,))

        top_users_by_word = c.fetchall()

        response = "The users that most use this word are:\n"
        response += "{:<30} {:<5}\n".format("User", "Count")
        for user in top_users_by_word:
            response += "{:<30} {:<5}\n".format(user[0], user[1])

        await send_message(message, response)
    
    except sqlite3.Error as e:
        print("Error retrieving top words by user:", e)
    finally:
        conn.close()


#########################################
async def get_top_words_by_channel(message):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        channel = message.content[15:]
        channel = channel.lower()
        channel = channel.replace(" ","")
        channel = transform_channel(channel)
        print(channel)

         # Check if the channel exists
        c.execute("SELECT channel_id FROM channels WHERE channel_name = ?", (channel,))
        channel_id = c.fetchone()
        if not channel_id:
            return "That channel doesn't exist"

        # Query to get the top 10 words by channel
        c.execute("""
            SELECT w.word, cw.count
            FROM channelwords cw
            JOIN words w ON cw.word_id = w.word_id
            JOIN channels c ON cw.channel_id = c.channel_id
            WHERE c.channel_name = ?
            ORDER BY cw.count DESC
            LIMIT 10
        """, (channel,))

        top_words_by_channel = c.fetchall()

        response = "The most used words written in this channel are:\n"
        response += "{:<30} {:<5}\n".format("Word", "Count")
        for word in top_words_by_channel:
            response += "{:<30} {:<5}\n".format(word[0], word[1])
        
        await send_message(message, response)

    except sqlite3.Error as e:
        print("Error retrieving top words by channel:", e)
    finally:
        conn.close()


##################################################
async def get_top_words_by_user(message):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        username = message.content[12:]
        username = username.lower()
        username = username.replace(" ","")
        print(username)

        # Check if the user exists
        c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user_id = c.fetchone()
        if not user_id:
            return "That user doesn't exist"

        # Query to get the top 10 words by user
        c.execute("""
            SELECT w.word, uw.count
            FROM userwords uw
            JOIN words w ON uw.word_id = w.word_id
            JOIN users u ON uw.user_id = u.user_id
            WHERE u.username = ?
            ORDER BY uw.count DESC
            LIMIT 10
        """, (username,))

        top_words_by_user = c.fetchall()

        response = "The most used words by this user are:\n"
        response += "{:<30} {:<5}\n".format("Word", "Count")
        for word in top_words_by_user:
            response += "{:<30} {:<5}\n".format(word[0], word[1])
        
        await send_message(message, response)

    except sqlite3.Error as e:
        print("Error retrieving top words by user:", e)
    finally:
        conn.close()


################################################
async def get_top_words_general(message):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        # Query to get the top 10 words with the highest count
        c.execute("SELECT word, count FROM words ORDER BY count DESC LIMIT 10")
        top_words = c.fetchall()

        conn.commit()

        response = "The most used words in this discord server are:\n"
        response += "Word".ljust(15) + "Count\n"
        response += "-" * 20 + "\n"
        for word in top_words:
            response += word[0].ljust(15) + str(word[1]).rjust(5) + "\n"

        await send_message(message, response)
    
    except sqlite3.Error as e:
        print("Error retrieving top words:", e)
    finally:
        conn.close()


#######################################################
def transform_channel(channel):
    try:
        conn = sqlite3.connect("wordstats.db")
        c = conn.cursor()

        c.execute("SELECT channel_name FROM channels")
        all_channels = c.fetchall()

        for ch in all_channels:
            ch_str = ch[0]
            if channel in ch_str:
                return ch_str
    except Exception as e:
        print("Error:", e)

    return channel