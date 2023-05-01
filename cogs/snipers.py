# shit code that works

import re
import discord
import aiohttp
import config
from discord.ext import commands as vbot
from colorama import Fore
from main import token
from time import perf_counter
from utils.req import __api__


class Snipers(
        vbot.Cog,
        name="Snipers"):
    def __init__(self, bot: vbot.Bot):
        self.bot = bot
        self.nitro_reg = re.compile(
            "(discord.gift/|discord.com/gifts/|discordapp.com/gifts/)([a-zA-Z0-9]+)")
        self.invite_reg = re.compile(
            "(https://discord.gg/|https://discord.com/invite/|discord.gg/)([a-zA-Z0-9]+)")

        try:
            self.session = aiohttp.ClientSession()
            self.nitro_webhook = discord.Webhook.from_url(
                config.snipers["nitro_sniper"]["url"], session=self.session)
            self.invite_webhook = discord.Webhook.from_url(
                config.snipers["invite_sniper"]["url"], session=self.session)
            self.keyword_webhook = discord.Webhook.from_url(
                config.snipers["keyword_sniper"]["url"], session=self.session)

        except:
            pass

    async def snipe_server(self, code: str, msg: discord.Message, r, r_delay: float):
        text = str(r)

        if not config.snipers["nitro_sniper"]["url"].startswith("https://discord.com/api/webhooks/"):
            if "This gift has been redeemed already" in text:
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mAlready Redemeed\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

            elif "Unknown Gift Code" in text:
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mInvalid Code\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

            elif "nitro" in text:
                print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mSuccesfully redeemed\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTGREEN_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

        else:
            if "This gift has been redeemed already" in text:
                embed = discord.Embed(color=0xff434b)
                embed.title = "Already Redeemed"
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  Server: {msg.guild.name}\n  Channel: #{msg.channel.name}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mAlready Redemeed\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.nitro_webhook.send(
                    content="@everyone" if config.snipers["nitro_sniper"]["ping"] else None,
                    embed=embed,
                    username="VSniper",
                    avatar_url="https://i.redd.it/0037pi1sppm71.png")

            elif "Unknown Gift Code" in text:
                embed = discord.Embed(color=0xff434b)
                embed.title = "Invalid Code"
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  Server: {msg.guild.name}\n  Channel: #{msg.channel.name}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mInvalid Code\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.nitro_webhook.send(
                    content="@everyone" if config.snipers["nitro_sniper"]["ping"] else None,
                    embed=embed,
                    username="VSniper",
                    avatar_url="https://i.redd.it/0037pi1sppm71.png")

            elif "nitro" in text:
                embed = discord.Embed(color=0xc3e88d)
                embed.title = "Succesfully redeemed"
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  Server: {msg.guild.name}\n  Channel: #{msg.channel.name}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mSuccesfully redeemed\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}" +
                      f"{Fore.LIGHTGREEN_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.nitro_webhook.send(
                    content="@everyone" if config.snipers["nitro_sniper"]["ping"] else None,
                    embed=embed,
                    username="VSniper",
                    avatar_url="https://i.redd.it/0037pi1sppm71.png")

    async def snipe_dm(self, code: str, msg: discord.Message, r, r_delay: float):
        text = str(r)

        if not config.snipers["nitro_sniper"]["url"].startswith("https://discord.com/api/webhooks/"):
            if "This gift has been redeemed already" in text:
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mAlready Redemeed\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

            elif "Unknown Gift Code" in text:
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mInvalid Code\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

            elif "nitro" in text:
                print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mSuccesfully redeemed\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTGREEN_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

        else:
            if "This gift has been redeemed already" in text:
                embed = discord.Embed(color=0xff434b)
                embed.title = "Already Redeemed"
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  DMs: {str(msg.channel).replace('Direct Message with', '')}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mAlready Redemeed\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.nitro_webhook.send(
                    content="@everyone" if config.snipers["nitro_sniper"]["ping"] else None,
                    embed=embed,
                    username="VSniper",
                    avatar_url="https://i.redd.it/0037pi1sppm71.png")

            elif "Unknown Gift Code" in text:
                embed = discord.Embed(color=0xff434b)
                embed.title = "Invalid Code"
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  DMs: {str(msg.channel).replace('Direct Message with', '')}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTRED_EX}[-] \033[1mInvalid Code\033[0m{Fore.LIGHTRED_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTRED_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTRED_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.nitro_webhook.send(
                    content="@everyone" if config.snipers["nitro_sniper"]["ping"] else None,
                    embed=embed,
                    username="VSniper",
                    avatar_url="https://i.redd.it/0037pi1sppm71.png")

            elif "nitro" in text:
                embed = discord.Embed(color=0xc3e88d)
                embed.title = "Succesfully redeemed"
                embed.url = msg.jump_url
                embed.description = f"""```yaml\n
- Code: {code}
- Sniped at:
  DMs: {str(msg.channel).replace('Direct Message with', '')}\n  By: {msg.author} ({msg.author.id})

- Delay: {str(r_delay)}```"""
                print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mSuccesfully redeemed\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}" +
                      f"{Fore.LIGHTGREEN_EX}\nDelay: " + r_delay + "\n" + Fore.RESET)

                await self.nitro_webhook.send(
                    content="@everyone" if config.snipers["nitro_sniper"]["ping"] else None,
                    embed=embed,
                    username="VSniper",
                    avatar_url="https://i.redd.it/0037pi1sppm71.png")

    async def claim_code(self, code: str, msg: discord.Message):
        async with aiohttp.ClientSession() as client:
            start = perf_counter()
            async with await client.post(
                    f"{__api__}/entitlements/gift-codes/{code}/redeem",
                    json={
                        "channel_id": str(msg.channel.id)
                    }, headers={
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
        if config.snipers["nitro_sniper"]["enabled"]:
            if self.nitro_reg.search(msg.content):
                if config.snipers["nitro_sniper"]["ignore_self"] and msg.author == self.bot.user:
                    return
                
                code = self.nitro_reg.search(msg.content).group(2)
                await self.claim_code(code, msg)
                self.bot.nitro_sniped += 1
        
        if config.snipers["invite_sniper"]["enabled"]:
            if self.invite_reg.search(msg.content):
                if msg.author.discriminator == "0000":
                    return
                if config.snipers["invite_sniper"]["ignore_limit"] != 0 and msg.guild.member_count >= config.snipers["invite_sniper"]["ignore_limit"]:
                    return
                if config.snipers["invite_sniper"]["ignore_self"] and msg.author == self.bot.user:
                    return
                
                code = self.invite_reg.search(msg.content).group(2)
                if isinstance(msg.channel, discord.DMChannel) or isinstance(msg.channel, discord.GroupChannel):
                    if not config.snipers["invite_sniper"]["url"].startswith("https://discord.com/api/webhooks/"):
                        print(f"{Fore.LIGHTGREEN_EX}[+] \033[1Found invite\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1mhttps://discord.gg/{code}\033[0m{Fore.LIGHTGREEN_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}")
                    
                    else:
                        
                        embed = discord.Embed(color=0xc3e88d)
                        embed.title = "Found invite"
                        embed.url = msg.jump_url
                        embed.description = f"""```yaml\n- Code: {code}
- Found at:
DMs: {str(msg.channel).replace('Direct Message with', '')}\n  By: {msg.author} ({msg.author.id})```"""

                        await self.invite_webhook.send(
                            content=f"{'@everyone - ' if config.snipers['invite_sniper']['ping'] else ''}https://discord.gg/{code}",
                            embed=embed,
                            username="VSniper",
                            avatar_url="https://i.redd.it/0037pi1sppm71.png")

                        print(f"{Fore.LIGHTGREEN_EX}[+] \033[1Found invite\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1m{code}\033[0m{Fore.LIGHTGREEN_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}")
                
                else:
                    if not config.snipers["invite_sniper"]["url"].startswith("https://discord.com/api/webhooks/"):
                        print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mFound invite\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1mhttps://discord.gg/{code}\033[0m{Fore.LIGHTGREEN_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}")
                    
                    else:
                        
                        embed = discord.Embed(color=0xc3e88d)
                        embed.title = "Found invite"
                        embed.url = msg.jump_url
                        embed.description = f"""```yaml\n- Code: {code}
- Sniped at:
  Server: {msg.guild.name}\n  Channel: #{msg.channel.name}\n  By: {msg.author} ({msg.author.id})```"""

                        await self.invite_webhook.send(
                            content=f"{'@everyone - ' if config.snipers['invite_sniper']['ping'] else ''}https://discord.gg/{code}",
                            embed=embed,
                            username="VSniper",
                            avatar_url="https://i.redd.it/0037pi1sppm71.png")

                        print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mFound invite\033[0m{Fore.LIGHTGREEN_EX} | Code: \033[1mhttps://discord.gg/{code}\033[0m{Fore.LIGHTGREEN_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}")

                self.bot.invites_found += 1
                
        if config.snipers["keyword_sniper"]["enabled"]:
            check = [keyword for keyword in config.snipers["keyword_sniper"]["keywords"] if(keyword.lower() in msg.content.lower())]
            if check != []:  
                if config.snipers["keyword_sniper"]["ignore_limit"] != 0 and msg.guild.member_count >= config.snipers["keyword_sniper"]["ignore_limit"]:
                    return
                if config.snipers["keyword_sniper"]["ignore_self"] and msg.author == self.bot.user:
                    return
                
                if isinstance(msg.channel, discord.DMChannel) or isinstance(msg.channel, discord.GroupChannel):
                    if not config.snipers["keyword_sniper"]["url"].startswith("https://discord.com/api/webhooks/"):
                        print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mFound keywords\033[0m{Fore.LIGHTGREEN_EX} | Keywords: \033[1m{', '.join(check)}\033[0m{Fore.LIGHTGREEN_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}")
                    
                    else:
                        embed = discord.Embed(color=0xc3e88d)
                        embed.title = "Found keywords"
                        embed.url = msg.jump_url
                        embed.description = f"""```yaml\n- Keywords: {', '.join(check)}
- Found at:
  DMs: {str(msg.channel).replace('Direct Message with', '')}\n  By: {msg.author} ({msg.author.id})```"""

                        await self.keyword_webhook.send(
                            content="@everyone" if config.snipers["keyword_sniper"]["ping"] else None,
                            embed=embed,
                            username="VSniper",
                            avatar_url="https://i.redd.it/0037pi1sppm71.png")

                        print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mFound keywords\033[0m{Fore.LIGHTGREEN_EX} | Keywords: \033[1m{', '.join(check)}\033[0m{Fore.LIGHTGREEN_EX} | DMs > {str(msg.channel).replace('Direct Message with', '')}")

                else:
                    if not config.snipers["keyword_sniper"]["url"].startswith("https://discord.com/api/webhooks/"):
                        print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mFound keywords\033[0m{Fore.LIGHTGREEN_EX} | Keywords: \033[1m{', '.join(check)}\033[0m{Fore.LIGHTGREEN_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}")
                    
                    else:
                        embed = discord.Embed(color=0xc3e88d)
                        embed.title = "Found keywords"
                        embed.url = msg.jump_url
                        embed.description = f"""```yaml\n- Keywords: {', '.join(check)}
- Sniped at:
  Server: {msg.guild.name}\n  Channel: #{msg.channel.name}\n  By: {msg.author} ({msg.author.id})```"""

                        await self.keyword_webhook.send(
                            content="@everyone" if config.snipers["keyword_sniper"]["ping"] else None,
                            embed=embed,
                            username="VSniper",
                            avatar_url="https://i.redd.it/0037pi1sppm71.png")

                        print(f"{Fore.LIGHTGREEN_EX}[+] \033[1mFound keywords\033[0m{Fore.LIGHTGREEN_EX} | Keywords: \033[1m{', '.join(check)}\033[0m{Fore.LIGHTGREEN_EX} | {msg.guild.name} > #{msg.channel.name} || {msg.author}")

                self.bot.keywords_found += 1

            # future invite sniper
            # reg = re.compile("(https://discord.gg/|https://discord.com/invite/|discord.gg/)([a-zA-Z0-9]+)")

            # if reg.search(msg.content):
            #   code = str(reg.search(msg.content).group(0))
            #   print(code)


async def setup(bot):
    sniper = Snipers(bot)
    await bot.add_cog(sniper)
