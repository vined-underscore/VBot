# shit code that works

import re
import selfcord as discord
import aiohttp
import config
import asyncio
from config import nitro_sniper_url
from selfcord.ext import commands as vbot
from colorama import Fore
from main import token
from time import perf_counter
from utils.req import __api__


class NitroSniper(
        vbot.Cog,
        name="Nitro Sniper"):
    def __init__(self, bot):
        self.bot: vbot.Bot = bot
        self.reg = re.compile(
            "(discord.gift/|discord.com/gifts/|discordapp.com/gifts/)([a-zA-Z0-9]+)")

        try:
            self.session = aiohttp.ClientSession()
            self.webhook = discord.Webhook.from_url(
                nitro_sniper_url, session=self.session)

        except:
            pass

    async def snipe_server(self, code: str, msg: discord.Message, r, r_delay: float):
        text = str(r)

        if not nitro_sniper_url.startswith('https://discord.com/api/webhooks/'):
            if 'This gift has been redeemed already' in text:
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mAlready Redemeed\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

            elif 'Unknown Gift Code' in text:
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mInvalid Code\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

            elif "nitro" in text:
                print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mSuccesfully redeemed\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTGREEN_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

        else:
            if 'This gift has been redeemed already' in text:
                embed = discord.Embed(color=0xff434b)
                embed.title = 'Already Redeemed'
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  Server: {msg.guild.name}\n  Channel: #{msg.channel.name}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mAlready Redemeed\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.webhook.send(
                    content="@everyone",
                    embed=embed,
                    username='VSniper',
                    avatar_url='https://i.redd.it/0037pi1sppm71.png')

            elif 'Unknown Gift Code' in text:
                embed = discord.Embed(color=0xff434b)
                embed.title = 'Invalid Code'
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  Server: {msg.guild.name}\n  Channel: #{msg.channel.name}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mInvalid Code\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.webhook.send(
                    content="@everyone",
                    embed=embed,
                    username='VSniper',
                    avatar_url='https://i.redd.it/0037pi1sppm71.png')

            elif "nitro" in text:
                embed = discord.Embed(color=0xc3e88d)
                embed.title = 'Succesfully redeemed'
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  Server: {msg.guild.name}\n  Channel: #{msg.channel.name}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mSuccesfully redeemed\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTGREEN_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.webhook.send(
                    content="@everyone",
                    embed=embed,
                    username='VSniper',
                    avatar_url='https://i.redd.it/0037pi1sppm71.png')

    async def snipe_dm(self, code: str, msg: discord.Message, r, r_delay: float):
        text = str(r)

        if not nitro_sniper_url.startswith('https://discord.com/api/webhooks/'):
            if 'This gift has been redeemed already' in text:
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mAlready Redemeed\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

            elif 'Unknown Gift Code' in text:
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mInvalid Code\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

            elif "nitro" in text:
                print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mSuccesfully redeemed\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTGREEN_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

        else:
            if 'This gift has been redeemed already' in text:
                embed = discord.Embed(color=0xff434b)
                embed.title = 'Already Redeemed'
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  DMs: {str(msg.channel).replace('Direct Message with', '')}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mAlready Redemeed\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.webhook.send(
                    content="@everyone",
                    embed=embed,
                    username='VSniper',
                    avatar_url='https://i.redd.it/0037pi1sppm71.png')

            elif 'Unknown Gift Code' in text:
                embed = discord.Embed(color=0xff434b)
                embed.title = 'Invalid Code'
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  DMs: {str(msg.channel).replace('Direct Message with', '')}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mInvalid Code\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.webhook.send(
                    content="@everyone",
                    embed=embed,
                    username='VSniper',
                    avatar_url='https://i.redd.it/0037pi1sppm71.png')

            elif "nitro" in text:
                embed = discord.Embed(color=0xc3e88d)
                embed.title = 'Succesfully redeemed'
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  DMs: {str(msg.channel).replace('Direct Message with', '')}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mSuccesfully redeemed\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTGREEN_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.webhook.send(
                    content="@everyone",
                    embed=embed,
                    username='VSniper',
                    avatar_url='https://i.redd.it/0037pi1sppm71.png')

    async def claim_code(self, code: str, msg: discord.Message):
        async with aiohttp.ClientSession() as client:
            start = perf_counter()
            async with await client.post(
                    f"{__api__}/entitlements/gift-codes/{code}/redeem",
                    json={
                        "channel_id": str(msg.channel.id)
                    },
                    headers={
                        "authorization": token
                    }) as r:
                end = perf_counter()
                c = await r.text()

                delay = end - start
                r_delay = "%.3fs" % delay

                if isinstance(msg.channel, discord.DMChannel):
                    await self.snipe_dm(code, msg, c, r_delay)

                elif isinstance(msg.channel, discord.GroupChannel):
                    await self.snipe_dm(code, msg, c, r_delay)

                else:
                    await self.snipe_server(code, msg, c, r_delay)

    @vbot.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if config.nitro_sniper:
            if self.reg.search(msg.content):
                code = self.reg.search(msg.content).group(2)

                await self.claim_code(code, msg)

            # future invite sniper
            # reg = re.compile("(https://discord.gg/|https://discord.com/invite/|discord.gg/)([a-zA-Z0-9]+)")

            # if reg.search(msg.content):
            #   code = str(reg.search(msg.content).group(0))
            #   print(code)


async def setup(bot):
    sniper = NitroSniper(bot)
    await bot.add_cog(sniper)
