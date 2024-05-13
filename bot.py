import discord
from discord.ext import commands
import time
from Methods import response_Handle
from utils import utils
from DataBase import DBupdate
from DataBase import DBquery
from Methods import command_Handle
from Methods import stats_handle

from utils.state import STATE

state = STATE.NORMAL
div_intensity = 1
message_count = 0
timestamp = None

########################################################
def run_discord_bot():
    global state
    global div_intensity

    # Discord Code - Ainda nao vi a documentaçao
    TOKEN = ''
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents = intents)
    
    # Events
    @bot.event
    async def on_ready():
        print(f'{bot.user} is running!')
        # Get the guild object
        guild = bot.guilds[0]  # Assuming your bot is in only one guild
        # await utils.get_history_all_channels(guild)

    # On Message
    @bot.event
    async def on_message(message):
        try:
            await bot.process_commands(message)
        except:
            print("OK")
        # Aqui devia dar return se processou algum comando

        try:
            global state
            global div_intensity

            # ignore messages by bot
            if message.author == bot.user:
                await dont_let_spam(message)
                return
            
            # FOR DEBUG
            if str(message.author) != "ruimachado":
                return
            
            # Update stats
            # stats_handle.update_stats(message)

            # Sleeping
            if state == STATE.SLEEP:
                return

            # Check Cheats
            if await utils.checkForCheats(message):
                return

            # Mention the Bot
            if bot.user.mentioned_in(message):
                await utils.respond_mention(message)  
                return

            await response_Handle.handle_Responses(message, div_intensity)

        except Exception as e:
            print(e)


    # Commands
    @bot.command()
    async def acorda(ctx):
        global state
        await command_Handle.wakeup(ctx.message, state)
        state = STATE.NORMAL

    @bot.command()
    async def vaidormir(message):
        global state
        await command_Handle.vaidormir(message)
        state = STATE.SLEEP

    @bot.command()
    async def nuke(message):
        await command_Handle.respond_nuke(message)

    @bot.command()
    async def defuse(message):
        await command_Handle.respond_defuse(message)

    @bot.command()
    async def intensity(message, arg):
        global div_intensity
        div_intensity = await command_Handle.change_intensity(message, arg)

    @bot.command()
    async def roast(ctx):
        mentioned_users = ctx.message.mentions
        if bot.user.mentioned_in(ctx.message):
            await ctx.channel.send("Querias que eu fizesse roast a mim próprio?")
            await command_Handle.self_roast(ctx.message)
            return
        if mentioned_users:
            await command_Handle.handle_roast(ctx.message)
        else:
            await ctx.channel.send("Dou roast a quem? Seu burro!")

    @bot.command()
    async def vocabulary(ctx, arg):
        await ctx.channel.send(ctx.author)
        await ctx.channel.send(arg)
        DBupdate.update_vocabulary(arg, str(ctx.author))

    # Commands Stats
    @bot.command()
    async def stats(message):
        stats_handle.get_top_words_general(message)

    @bot.command()
    async def stats_user(message):
        stats_handle.get_top_words_by_user(message)

    @bot.command()
    async def stats_word(message):
        stats_handle.get_top_users_by_word(message)

    @bot.command()
    async def stats_channel(message):
        stats_handle.get_top_words_by_channel(message)


    #################
    bot.run(TOKEN)


####################################################################
async def dont_let_spam(message):
    global timestamp
    global message_count
    global div_intensity
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
            div_intensity = 1
            time.sleep(180)
            await message.channel.send("Voltei caralho")
            
        message_count = 0
        timestamp = current_time















    



#################################################################################3
if __name__ == '__main__':
    run_discord_bot()
