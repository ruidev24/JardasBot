from discord.ext import commands

from database import DBgeneral
from methods.response_handlers import (
    respond_self_roast,
    respond_roast,
    respond_fortune,
    respond_vocabulary
)


##############################################################################
async def handle_roast(bot: commands.Bot, ctx: commands.Context):
    mentioned_users = ctx.message.mentions

    if bot.user.mentioned_in(ctx.message):
        await respond_self_roast(ctx)
    elif mentioned_users:
        await respond_roast(ctx)
    else:
        await ctx.channel.send("Dou roast a quem? Seu burro!")


async def handle_fortune(ctx: commands.Context):
    allowed = DBgeneral.get_fortune_allowed(ctx.author)
    if not allowed:
        await ctx.channel.send("Só tens direito a 1 por semana caralho")
    else:
        await respond_fortune(ctx)
        DBgeneral.update_fortune_allowed(ctx.author)


async def handle_vocabulary(ctx: commands.Context, arg):
    DBgeneral.update_vocabulary(arg, str(ctx.author))
    await respond_vocabulary(ctx)

