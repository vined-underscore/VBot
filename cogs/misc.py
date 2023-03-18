import selfcord as discord
import random
import main
import config
from colorama import Fore as F
from selfcord.ext import commands as vbot
from utils import other
from utils import alias
from cogs import events

class MiscCmds(
    vbot.Cog,
    name = "Misc",
    description = "Various miscellanous commands"):
  def __init__(self, bot):
    self.bot = bot

  @vbot.command(
    name="listening",
    description="Sets your status to Listening"
  )
  async def listening(self, ctx, *, activity_message):
    msg = ctx.message
      
    await self.bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=activity_message,))
    
    await msg.edit(content = f"```yaml\n+ Set your listening status to {activity_message}```", delete_after = 5)

  @vbot.command(
    name="watching",
    description="Sets your status to Watching"
  )
  async def watching(self, ctx, *, activity_message):
    msg = ctx.message
      
    await self.bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.watching, 
        name=activity_message))
    
    await msg.edit(content = f"```yaml\n+ Set your watching status to {activity_message}```", delete_after = 5)

  @vbot.command(
    name="streaming",
    description="Sets your status to Streaming"
  )
  async def streaming(self, ctx, stream_url=None, *, activity_message):
    msg = ctx.message
      
    stream_urls = [
        "https://m.twitch.tv/dream"
    ]
    
    if not stream_url:
        stream_url = random.choice(stream_urls)
      
    await self.bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.streaming,
        name=activity_message,
        url=stream_url))
    
    await msg.edit(content = f"```yaml\n+ Set your streaming status to {activity_message} (Redirect: {stream_url})```", delete_after = 5)

  @vbot.command(
    name="playing",
    description="Sets your status to Playing"
  )
  async def playing(self, ctx, *, activity_message):
    msg = ctx.message
  
    await self.bot.change_presence(
        activity=discord.Activity(
        type=discord.ActivityType.playing,
        name=activity_message))
    
    await msg.edit(content=f"```yaml\n+ Set your playing status to {activity_message}```", delete_after = 5)

  @vbot.command(
    name = "stopactivity",
    description = "Stops your current activity",
    aliases = alias.get_aliases("stopactivity")
  )
  async def stopactivity(self, ctx):
    await ctx.message.delete()
    await self.bot.change_presence(activity = None)
    
  @vbot.group(
    name = "status",
    description = "Changes your status",
    invoke_without_command = True
  )
  async def status(self, ctx):
    msg = ctx.message
    await msg.edit(content=f"```yaml\n- Incorrect usage. Correct usage: {ctx.clean_prefix}help [status]```", delete_after = 5)
    
  @status.command(
    name = "dnd",
    description = "Changes your status to do not disturb"
  )
  async def dnd(self, ctx):
    msg = ctx.message
    await self.bot.change_presence(status=discord.Status.dnd)
    await msg.edit(content=f"```yaml\nChanged status to do not disturb.```", delete_after = 5)
    
  @status.command(
    name = "idle",
    description = "Changes your status to idle"
  )
  async def idle(self, ctx):
    msg = ctx.message
    await self.bot.change_presence(status=discord.Status.idle)
    await msg.edit(content=f"```yaml\nChanged status to idle.```", delete_after = 5)

  @status.command(
    name = "offline",
    description = "Changes your status to offline"
  )
  async def offline(self, ctx):
    msg = ctx.message
    await self.bot.change_presence(status=discord.Status.invisible)
    await msg.edit(content=f"```yaml\nChanged status to offline```", delete_after = 5)

  @status.command(
    name = "online",
    description = "Changes your status to online"
  )
  async def online(self, ctx):
    msg = ctx.message
    await self.bot.change_presence(status=discord.Status.dnd)
    await msg.edit(content=f"```yaml\nChanged status to online.```", delete_after = 5)
    
  @status.command(
    name = "none",
    description = "Changes your status to none (Gives priority over your discord app status)"
  )
  async def none(self, ctx):
    msg = ctx.message
    await self.bot.change_presence(status=None)
    await msg.edit(content=f"```yaml\nChanged status to none.```", delete_after = 5)
  
  @vbot.command(
    name = "clearconsole",
    description = "Clears the console"
  )
  async def clearconsole(self, ctx):
    await ctx.message.delete()
    
    other.clear_console()
    events.banner(self.bot)
    print(f"{F.LIGHTBLACK_EX}Logged in as {F.LIGHTBLUE_EX}{self.bot.user}{F.LIGHTBLACK_EX} with {'prefix ' + F.LIGHTCYAN_EX + main.prefix[0] if len(main.prefix) == 1 else 'prefixes ' + F.LIGHTCYAN_EX + f' {F.LIGHTBLACK_EX}|{F.LIGHTCYAN_EX} '.join(main.prefix)}\n")
    
    print(f"{F.LIGHTYELLOW_EX}(?){F.LIGHTWHITE_EX} Nitro Sniper enabled: {F.LIGHTRED_EX if config.nitro_sniper == False else F.LIGHTGREEN_EX}{config.nitro_sniper}")
    if config.nitro_sniper:
      print(f"{F.LIGHTGREEN_EX}(+){F.LIGHTWHITE_EX} Nitro sniping {len(self.bot.guilds)} servers\n")

  @vbot.command(
    name = "ping",
    description = "Sends the bot latency",
    aliases = alias.get_aliases("ping")
  )
  async def ping(self, ctx):
    msg = ctx.message
    latency = round(self.bot.latency * 1000)
    
    await msg.edit(content = f"```yaml\nThe bot's latency is {latency}ms```", delete_after = 5)

if __name__ == "__main__":
    print("You need to run main.py to run the bot")

async def setup(bot):
  await bot.add_cog(MiscCmds(bot))