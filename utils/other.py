import os
import discord
import config
import traceback
import sys
from discord.ext import commands
from datetime import datetime
from colorama import Fore as F
from typing import Any, Union


def clear_console() -> None:
    os.system("clear" if os.name != "nt" else "cls")


def log(text: Any) -> None:
    now = datetime.now()
    time = now.strftime("%H:%M:%S %d-%m-%Y")
    print(f"{F.LIGHTBLACK_EX}[{time}] {text}")


async def log_error(ctx: commands.Context, error, message: str, unknown: bool = False) -> None:
    if config.logging["error_logging"] == "console":
        if unknown:
            return

        log(f"{F.RED}An error has occured in command {F.LIGHTBLUE_EX}\"{ctx.message.content}\"{F.RED}:")
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr)
        print("\n")
        await ctx.message.delete()

    elif config.logging["error_logging"] == "channel":
        await ctx.message.edit(content=message, delete_after=5)

    elif config.logging["error_logging"] == "both":
        msg = ctx.message.content
        await ctx.message.edit(content=message, delete_after=5)

        if unknown:
            return

        log(f"{F.RED}An error has occured in command {F.LIGHTBLUE_EX}\"{msg}\"{F.RED}:")
        traceback.print_exception(
            type(error), error, error.__traceback__, file=sys.stderr)
        print("\n")

    else:
        await ctx.message.delete()


def get_first_channel(guild: discord.Guild) -> Union[discord.TextChannel, str]:
    channels = [channel for channel in guild.text_channels if channel.permissions_for(
        guild.me).read_messages]
    if channels != []:
        return channels[0]
    else:
        return "Couldn't get link"
