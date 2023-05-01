import discord 
import asyncio
import config
import os
import aiohttp
import fade
import platform
import logging
import logging.handlers
import colorama
import time
import datetime
from utils import other
from colorama import Fore as F
from typing import List
from discord.ext import commands
colorama.init()

token = config.token
prefix = config.prefix

__version__ = "3.4.3"
__author_id__ = 851442209021493268  # No skid pls
__cog_folder__ = "cogs"  # Change this if you ever rename the "cogs" folder


class VBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        web_client: aiohttp.ClientSession,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.web_client = web_client
        self.initial_extensions = initial_extensions
        self.start_time = None
        self.total_logs = 0
        self.total_msgs = 0
        self.total_cmds = 0
        self.nitro_sniped = 0
        self.invites_found = 0
        self.keywords_found = 0

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"{F.GREEN}[+]{F.LIGHTWHITE_EX} Loaded {extension}")

            except Exception as e:
                print(
                    f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to load {extension}.\n  Error: {F.RED}{e}{F.RESET}")
                exit()

        print(f"{F.YELLOW}[?]{F.LIGHTWHITE_EX} Connecting...")
        self.start_time = time.time()
        
    def get_uptime(self) -> str:
        uptime = round(time.time() - self.start_time)
        return str(datetime.timedelta(seconds = int(uptime)))
    
    def banner(self):
        author = self.get_user(__author_id__)
        print(fade.purpleblue(f"""

██╗   ██╗██████╗  ██████╗ ████████╗
██║   ██║██╔══██╗██╔═══██╗╚══██╔══╝
██║   ██║██████╔╝██║   ██║   ██║   
╚██╗ ██╔╝██╔══██╗██║   ██║   ██║   
 ╚████╔╝ ██████╔╝╚██████╔╝   ██║   
  ╚═══╝  ╚═════╝  ╚═════╝    ╚═╝                 
           v{__version__}"""))
        print(f"""
{F.LIGHTBLACK_EX}-> {F.LIGHTWHITE_EX}discord.py {F.LIGHTBLUE_EX}v{discord.__version__}{F.LIGHTBLACK_EX} <-      
  {F.LIGHTBLACK_EX}-> {F.LIGHTWHITE_EX}python {F.LIGHTBLUE_EX}v{platform.python_version()}{F.LIGHTBLACK_EX} <-

{F.LIGHTBLACK_EX}* {F.LIGHTWHITE_EX}Made by {F.LIGHTBLUE_EX}{author}{F.LIGHTBLACK_EX}
{F.LIGHTBLACK_EX}* {F.LIGHTBLUE_EX}{len([command for command in self.walk_commands()])} {F.LIGHTWHITE_EX}commands and subcommands""")
    
    def full_banner(self):
        other.clear_console()
        self.banner()
        print(
            f"{F.LIGHTBLACK_EX}Logged in as {F.LIGHTBLUE_EX}{self.user}{F.LIGHTBLACK_EX} with {'prefix ' + F.LIGHTCYAN_EX + main.prefix[0] if len(prefix) == 1 else 'prefixes ' + F.LIGHTCYAN_EX + f' {F.LIGHTBLACK_EX}|{F.LIGHTCYAN_EX} '.join(prefix)}\n")

        print(f"{F.LIGHTYELLOW_EX}(?){F.LIGHTWHITE_EX} Server Logging enabled: {F.LIGHTRED_EX if config.logging['is_logging'] == False else F.LIGHTGREEN_EX}{config.logging['is_logging']}")
        print(f"{F.LIGHTYELLOW_EX}(?){F.LIGHTWHITE_EX} Error Logging: {F.LIGHTGREEN_EX}{config.logging['error_logging'] if config.logging['error_logging'] != '' else f'{F.RED}disabled'}\n")
        
        print(f"{F.LIGHTMAGENTA_EX}(*){F.LIGHTWHITE_EX} Snipers:")
        print(f"  {F.LIGHTYELLOW_EX}(?){F.LIGHTWHITE_EX} Nitro Sniper enabled: {F.LIGHTRED_EX if config.snipers['nitro_sniper']['enabled'] == False else F.LIGHTGREEN_EX}{config.snipers['nitro_sniper']['enabled']}")
        if config.snipers["nitro_sniper"]["enabled"]:
            print(f"  {F.LIGHTGREEN_EX}(+){F.LIGHTWHITE_EX} Nitro sniping {len(self.guilds)} servers\n")
        
        print(f"  {F.LIGHTYELLOW_EX}(?){F.LIGHTWHITE_EX} Invite Sniper enabled: {F.LIGHTRED_EX if config.snipers['invite_sniper']['enabled'] == False else F.LIGHTGREEN_EX}{config.snipers['invite_sniper']['enabled']}")
        if config.snipers["invite_sniper"]["enabled"]:
            print(f"  {F.LIGHTGREEN_EX}(+){F.LIGHTWHITE_EX} Invite sniping {len(self.guilds)} servers\n")
            
        print(f"  {F.LIGHTYELLOW_EX}(?){F.LIGHTWHITE_EX} Keyword Sniper enabled: {F.LIGHTRED_EX if config.snipers['keyword_sniper']['enabled'] == False else F.LIGHTGREEN_EX}{config.snipers['keyword_sniper']['enabled']}")
        if config.snipers["keyword_sniper"]["enabled"]:
            print(f"  {F.LIGHTGREEN_EX}(+){F.LIGHTWHITE_EX} Invite sniping {len(self.guilds)} servers")
            print(f"  {F.LIGHTGREEN_EX}(+){F.LIGHTWHITE_EX} Looking out for the words: {F.LIGHTBLUE_EX}{', '.join(config.snipers['keyword_sniper']['keywords'])}\n")
        
        
        
async def main():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,
        backupCount=5,
    )
    dt_fmt = "%H:%M:%S %d-%m-%Y"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    async with aiohttp.ClientSession() as client:
        exts = [
            f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs") if filename.endswith(".py")]
        async with VBot(
            command_prefix=prefix,
            case_insensitive=True,
            web_client=client,
            self_bot=True,
            initial_extensions=exts
        ) as bot:
            try:
                await bot.start(token)

            except discord.LoginFailure:
                print(
                    f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to login. The token is invalid.")

            except discord.ConnectionClosed:
                print(
                    f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to login because the discord gateway has been forcefully closed.")

            except discord.GatewayNotFound:
                print(
                    f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to login because there is most likely an API outage on Discord.")

            except discord.HTTPException:
                print(
                    f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to login due to a HTTP Exception.")

if __name__ == "__main__":
    asyncio.run(main())
