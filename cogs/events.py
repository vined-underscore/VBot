import selfcord as discord
import main
import fade
import platform
import config
from datetime import datetime
from colorama import Fore as F
from selfcord.ext import commands as vbot
from utils import other
from utils.msg import delete_msg

py_ver = platform.python_version()
bot_ver = main.__version__
discord_ver = discord.__version__

def banner(bot):
  author = bot.get_user(main.__author_id__)
  print(fade.purpleblue(f"""

██╗   ██╗██████╗  ██████╗ ████████╗
██║   ██║██╔══██╗██╔═══██╗╚══██╔══╝
██║   ██║██████╔╝██║   ██║   ██║   
╚██╗ ██╔╝██╔══██╗██║   ██║   ██║   
 ╚████╔╝ ██████╔╝╚██████╔╝   ██║   
  ╚═══╝  ╚═════╝  ╚═════╝    ╚═╝                              
"""))
  print(f"""
{F.LIGHTBLACK_EX}-> {F.LIGHTWHITE_EX}VBot {F.LIGHTBLUE_EX}v{main.__version__}    
{F.LIGHTBLACK_EX}-> {F.LIGHTWHITE_EX}discord.py {F.LIGHTBLUE_EX}v{discord_ver}        
{F.LIGHTBLACK_EX}-> {F.LIGHTWHITE_EX}Python {F.LIGHTBLUE_EX}v{py_ver}         
{F.LIGHTBLACK_EX}-> {F.LIGHTWHITE_EX}Made by {F.LIGHTBLUE_EX}{author}
{F.LIGHTBLACK_EX}-> {F.LIGHTBLUE_EX}{len([command for command in bot.walk_commands()])} {F.LIGHTWHITE_EX}commands and subcommands
""")

class Events(
    vbot.Cog,
    name = "Events"):
  def __init__(self, bot):
    self.bot = bot

  @vbot.Cog.listener()
  async def on_connect(self):
    other.clear_console()
    banner(self.bot)
    print(f"{F.LIGHTBLACK_EX}Logged in as {F.LIGHTBLUE_EX}{self.bot.user}{F.LIGHTBLACK_EX} with {'prefix ' + F.LIGHTCYAN_EX + main.prefix[0] if len(main.prefix) == 1 else 'prefixes ' + F.LIGHTCYAN_EX + f' {F.LIGHTBLACK_EX}|{F.LIGHTCYAN_EX} '.join(main.prefix)}\n")
    
    print(f"{F.LIGHTYELLOW_EX}(?){F.LIGHTWHITE_EX} Nitro Sniper enabled: {F.LIGHTRED_EX if config.nitro_sniper == False else F.LIGHTGREEN_EX}{config.nitro_sniper}")
    if config.nitro_sniper:
      print(f"{F.LIGHTGREEN_EX}(+){F.LIGHTWHITE_EX} Nitro sniping {len(self.bot.guilds)} servers\n")

  @vbot.Cog.listener()
  async def on_message_edit(self, before, after):
    await self.bot.process_commands(after)
      
  @vbot.Cog.listener()
  async def on_guild_remove(self, guild):
    if not config.logging: return
    
    now = datetime.now()
    time = now.strftime("%H:%M:%S %d-%m-%Y")
    print(f"{F.LIGHTBLACK_EX}[{time}] {F.RED}Left server {F.WHITE}| {F.LIGHTBLUE_EX}{guild.name} {F.LIGHTWHITE_EX}({guild.id})")
    
  @vbot.Cog.listener()
  async def on_guild_join(self, guild):
    if not config.logging: return
    
    now = datetime.now()
    time = now.strftime("%H:%M:%S %d-%m-%Y")
    print(f"{F.LIGHTBLACK_EX}[{time}] {F.GREEN}Joined server {F.WHITE}| {F.LIGHTBLUE_EX}{guild.name} {F.LIGHTWHITE_EX}({guild.id})")
    
  @vbot.Cog.listener()
  async def on_member_remove(self, member):
    if not config.logging: return
    
    now = datetime.now()
    time = now.strftime("%H:%M:%S %d-%m-%Y")
    if member == member.guild.me: return
    print(f"{F.LIGHTBLACK_EX}[{time}] {F.RED}User left a server {F.WHITE}| {F.LIGHTBLUE_EX}{member} - {member.guild.name} {F.LIGHTWHITE_EX}({member.id} - {member.guild.id})")
    
  @vbot.Cog.listener()
  async def on_member_join(self, member):
    if not config.logging: return
    
    now = datetime.now()
    time = now.strftime("%H:%M:%S %d-%m-%Y")
    if member == member.guild.me: return
    print(f"{F.LIGHTBLACK_EX}[{time}] {F.GREEN}User joined a server {F.WHITE}| {F.LIGHTBLUE_EX}{member} - {member.guild.name} {F.LIGHTWHITE_EX}(User: {member.id} - Server: {member.guild.id})")
    
  @vbot.Cog.listener()
  async def on_command(self, ctx: vbot.Context):
    if not config.logging: return
    cmd = ctx.command
    msg = ctx.message
    
    if cmd.name == "help":
        await delete_msg(msg)
    
    now = datetime.now()
    time = now.strftime("%H:%M:%S %d-%m-%Y")
    print(f"{F.LIGHTBLACK_EX}[{time}] {F.GREEN}Sent command {F.WHITE}| {F.LIGHTBLUE_EX}{msg.content} {F.LIGHTWHITE_EX}at {f'#{ctx.channel.name}' if not isinstance(ctx.channel, discord.DMChannel) else ctx.channel}")
  
if __name__ == "__main__":
    print("You need to run main.py to run the bot")

async def setup(bot):
  await bot.add_cog(Events(bot))
