import asyncio
import selfcord as discord
from selfcord.ext import commands as vbot

delay = 5

async def delete_msg(msg: discord.Message): # For some reason using
    await asyncio.sleep(delay) # await msg.edit(delete_after = 5)
    await msg.delete() # Makes a stupid loop

async def send_msg(msg: discord.Message, ctx: vbot.Context):
    await ctx.send(msg)
    await delete_msg(ctx.message, delay)