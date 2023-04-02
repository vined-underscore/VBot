import selfcord as discord
import asyncio
import config
import os
import aiohttp
import logging
import logging.handlers
from colorama import Fore as F
from typing import List
from selfcord.ext import commands

token = config.token
prefix = config.prefix

__version__ = "3.2.0"
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
            self_bot=True,  # FUCK
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
