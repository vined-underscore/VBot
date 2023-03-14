import os
import config
import asyncio
from colorama import Fore as F
from utils import other
from selfcord.ext import commands

token = config.token
prefix = config.prefix

__version__ = "3.0"
__author_id__ = 851442209021493268 # No skid pls
__cog_folder__ = "cogs" # Change this if you ever rename the "cogs" folder

vbot = commands.Bot(
  command_prefix=prefix,
  self_bot=True,
  case_insensitive=True
)

async def run_cogs():
  for filename in os.listdir(__cog_folder__):
    if filename.endswith('.py'):
      try:
        await vbot.load_extension(f'{__cog_folder__}.{filename[:-3]}')
        print(f'{F.GREEN}[+]{F.LIGHTWHITE_EX} Loaded {filename}')
      
      except Exception as e:
        print(f'{F.RED}[-]{F.LIGHTWHITE_EX} Failed to load {filename}. Error: {e}')
        exit()

async def main():
  await run_cogs()
  
  try:
    print("Connecting...")

    other.clear_console()
    await vbot.start(token)

  except Exception as e:
    print(f"Failed to login. Error: {e}")

if __name__ == "__main__":
  asyncio.run(main())
