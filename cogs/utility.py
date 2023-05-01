import datetime
import discord
import main
import asyncio
import aiohttp
import flag
from discord.ext import commands as vbot
from discord.ext import tasks
from colorama import Fore
from utils import req
from utils import alias
from utils.req import __api__
from datetime import datetime
from typing import Optional


class UtilityCmds(
        vbot.Cog,
        name="Utils",
        description="Various useful commands"):
    def __init__(self, bot: vbot.Bot):
        self.bot = bot
        self.is_clear = False
        self.snipe_message = {}
        self.snipe_message_edit = {}
        self.msgs = 0
        self.deleted = 0
        self.messages = []
        self.bump = {
            "bumping": False,
            "cmd_obj": None
        }

    @vbot.group(
        name="clear",
        description="Clears messages. Put an ID to specifically clear a channel",
        aliases=alias.get_aliases("clear"),
        invoke_without_command=True
    )
    async def clear(self, ctx: vbot.Context, amount: int, channel_id: Optional[int]):
        self.is_clear = True

        msg = ctx.message

        channel_id = channel_id or msg.channel.id
        channel = self.bot.get_channel(channel_id)

        if isinstance(channel, discord.GroupChannel) or isinstance(channel, discord.DMChannel):
            count = 0
            async for message in channel.history(limit=amount):
                if self.is_clear == False:
                    return
                if not message.author == self.bot.user:
                    continue
                if message == msg:
                    continue

                try:
                    await message.delete()
                    count += 1

                except:
                    pass

            await msg.edit(content=f"```yaml\n+ Deleted {count} messages.```", delete_after=5)

        else:
            def purge(m):
                return m.author == self.bot.user and m != msg

            deleted = await channel.purge(limit=amount, check=purge)

            self.is_clear = False
            await msg.edit(content=f"```yaml\n+ Deleted {len(deleted)} messages.```", delete_after=5)

    @clear.command(
        name="antireport",
        description="Deletes all messages by you in every server/dm that contain a specific string (Might take a while)",
        aliases=alias.get_aliases("antireport")
    )
    async def antireport(self, ctx: vbot.Context, *, messg: str):
        msg = ctx.message

        await msg.edit(content=f"""```yaml\nStarting purge process...```""")
        print(
            f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Starting antireport purge...\n")

        async def search_guild(self, guild):
            print(
                f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Moving over to server {Fore.LIGHTBLUE_EX}{guild.name}{Fore.LIGHTWHITE_EX}\n")

            if guild.member_count > 500:
                print(
                    f"{Fore.RED}[-]{Fore.LIGHTWHITE_EX} {Fore.LIGHTBLUE_EX}{guild.name}{Fore.LIGHTWHITE_EX} has more than 500 members, skipping...\n")
                return

            for channel in guild.text_channels:
                print(f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Looking through {Fore.LIGHTBLUE_EX}#{channel.name}{Fore.LIGHTWHITE_EX} in {Fore.LIGHTBLUE_EX}{guild.name}{Fore.LIGHTWHITE_EX}... ({self.msgs} messages so far)")

                if not channel.permissions_for(guild.me).send_messages:
                    print(
                        f"{Fore.RED}[-]{Fore.LIGHTWHITE_EX} User doesnt have message access in {Fore.LIGHTBLUE_EX}#{channel.name}{Fore.LIGHTWHITE_EX}, skipping...\n")
                    continue

                try:
                    async for message in channel.history(limit=None):
                        self.msgs += 1
                        if message.author == self.bot.user:
                            if messg.lower() in message.content.lower():
                                self.messages.append(message)
                                print(
                                    f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Found message with string \"{messg}\" in {Fore.LIGHTBLUE_EX}#{channel.name}{Fore.LIGHTWHITE_EX}")
                                await message.delete()
                                self.deleted += 1
                                await asyncio.sleep(1)

                except discord.Forbidden:
                    print(
                        f"{Fore.RED}[-]{Fore.LIGHTWHITE_EX} User doesnt have access in {Fore.LIGHTBLUE_EX}#{channel.name}{Fore.LIGHTWHITE_EX}, skipping...\n")
                    await asyncio.sleep(1)
                    continue

                except discord.HTTPException:
                    await asyncio.sleep(5)

                await asyncio.sleep(5)

        coros = [search_guild(self, guild) for guild in self.bot.guilds]
        await asyncio.gather(*coros)

        await msg.edit(content=f"""```yaml\nSuccesfully deleted {self.deleted}/{len(self.messages)} messages.```""", delete_after=15)
        self.msgs = 0
        self.deleted = 0
        self.messages = []

    @clear.command(
        name="stop",
        description="Stops the clear command"
    )
    async def stop(self, ctx: vbot.Context):
        msg = ctx.message

        if self.is_clear == False:
            await msg.edit(content="```yaml\n- There is no clear going on``", delete_after=5)

        else:
            self.is_clear = False
            await msg.edit(content="```yaml\n+ Stopped clear```", delete_after=5)

    @vbot.command(
        name="msgedit",
        description="Edits an amount of your messages in the channel"
    )
    async def msgedit(self, ctx: vbot.Context, amount: int, *, txt: str):
        msg = ctx.message
        channel = ctx.channel
        await msg.delete(delay=5)
        history = [m async for m in channel.history(limit=amount)]

        for message in history:
            if message.author == self.bot.user:
                await message.edit(content=txt)

    @vbot.group(
        name="info",
        description="Various commands to show information about things",
        invoke_without_command=True
    )
    async def info(self, ctx: vbot.Context):
        msg = ctx.message
        await msg.edit(content=f"```yaml\n- Incorrect usage. Correct usage: {ctx.clean_prefix}help [info]```", delete_after=5)

    @info.command(
        name="user",
        description="Saves user info of an user to the info folder (may not work if user has some non ascii characters in their name)",
        aliases=alias.get_aliases("user")
    )
    async def user(self, ctx: vbot.Context, user: Optional[discord.User]):
        msg = ctx.message
        user = user or ctx.author

        invalid_chars = "#%&{}\<>*?/ $!\":@+`|="
        username = str(user)
        for char in invalid_chars:
            if char in username:
                username = username.replace(char, "_")

        with open(f"./info/users/USER_INFO {username}.txt", "w", encoding="utf-8") as f:
            req = await self.bot.http.request(
                discord.http.Route(
                    "GET",
                    "/users/{uid}",
                    uid=user.id))

            banner_id = req["banner"]
            if banner_id:
                banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"

            else:
                pass

            now = datetime.now().astimezone()
            created_at = user.created_at
            days_ago = now - created_at

            info = f"""
- Username: {user.name}#{user.discriminator}
- User ID: {user.id}
- Created at: {created_at.strftime("%b %d %Y")} ({days_ago.days} days ago)
- Avatar URL: {user.avatar.url}
- Banner URL: {banner_url if banner_id else "None"}
- Public Flags: {user.public_flags.value}
- Is a bot: {user.bot}"""
            f.write(info)

        with open(f"./info/users/USER_INFO {username}.txt", "rb") as f:
            await ctx.send(content=f"```yaml\n{info}```", file=discord.File(f))

        await msg.delete(delay=5)

    @info.command(
        name="server",
        description="Saves server info of the current server (or by id) to the info folder (may not work if server has some non ascii characters in its name)",
        aliases=alias.get_aliases("server")
    )
    async def server(self, ctx: vbot.Context, server_id: Optional[int]):
        msg = ctx.message
        server_id = server_id or ctx.guild.id

        try:
            guild = self.bot.get_guild(server_id)

        except:
            return await ctx.send("```yaml\n- Error: Invalid server ID```", delete_after=5)

        invalid_chars = "#%&{}\<>*?/ $!\":@+`|="
        servername = str(guild.name)
        for char in invalid_chars:
            if char in servername:
                servername = servername.replace(char, "_")

        try:
            channel = guild.text_channels[0]
            invite = await channel.create_invite(max_age=0, max_uses=0)
            invite = str(invite)

        except:
            invite = "Couldn't make an invite"

        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        all_channels = len(guild.channels)

        roles = len(guild.roles)
        emojis = len(guild.emojis)
        members = guild.member_count
        owner = guild.owner

        req = await self.bot.http.request(
            discord.http.Route(
                "GET",
                "/users/{uid}",
                uid=owner.id))

        banner_id = req["banner"]
        if banner_id:
            banner_url = f"https://cdn.discordapp.com/banners/{owner.id}/{banner_id}?size=1024"

        else:
            pass

        with open(f"./info/servers/SERVER_INFO {servername}.txt", "w", encoding="utf-8") as f:
            now = datetime.now().astimezone()
            created_at_server = guild.created_at
            days_ago_server = now - created_at_server
            created_at_owner = owner.created_at
            days_ago_owner = now - created_at_owner
            info = f"""
- Server name: {guild.name}
- Server ID: {guild.id}
- Amount of text channels: {text_channels}
- Amount of voice channels: {voice_channels}
- Amount of categories: {categories}
- Amount of all channels: {all_channels}
- Amount of roles: {roles}
- Amount of emojis: {emojis}
- Amount of members: {members}
- Created at: {created_at_server.strftime("%b %d %Y")} ({days_ago_server.days} days ago)
- Icon URL: {guild.icon.url}
- Invite: {invite}

!= Owner information:
  - Username: {owner.name}#{owner.discriminator}
  - User ID: {owner.id}
  - Created at: {created_at_owner.strftime("%b %d %Y")} ({days_ago_owner.days} days ago)
  - Avatar URL: {owner.avatar.url}
  - Banner URL: {banner_url if banner_id else "None"}
  - Public Flags: {owner.public_flags.value}
  - Is a bot: {owner.bot}"""
            f.write(info)

        with open(f"./info/servers/SERVER_INFO {servername}.txt", "rb") as f:
            await ctx.send(content=f"```yaml\n{info}```", file=discord.File(f))

        await msg.delete(delay=5)

    @info.command(
        name="token",
        description="Gets information from a token (may not work if token has some non ascii characters in its name)"
    )
    async def token(self, ctx: vbot.Context, token: str):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r_user = await http.get(
                "https://discord.com/api/v9/users/@me",
                headers={
                    "authorization": token,
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9011 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36"
                })

            nitro_types = {
                "1": "Classic",
                "2": "Monthly"
            }

            try:
                js = await r_user.json()
                try:
                    n = nitro_types[str(js["premium_type"])]

                except Exception as e:
                    n = "None"

                invalid_chars = "#%&{}\<>*?/ $!'\":@+`|="
                username = f"{js['username']}#{str(js['discriminator'])}"
                for char in invalid_chars:
                    if char in username:
                        username = username.replace(char, "_")

                info = f"""- Token: {token}
- Username: {js["username"]}#{js["discriminator"]}
- ID: {js["id"]}
- Email: {js["email"]}
- Phone: {js["phone"]}
- Avatar URL: https://cdn.discordapp.com/avatars/{js["id"]}/{js["avatar"]}.png?size=2048
- Banner URL: https://cdn.discordapp.com/banners/{js["id"]}/{js["banner"]}.png?size=2048
- Bio: {None if js["bio"] == "" else js["bio"]}
- Locale: {js["locale"]}
- 2FA Enabled: {js["mfa_enabled"]}
- Verified: {js["verified"]}
- Nitro Subscription: {n}"""

                with open(f"./info/tokens/TOKEN_INFO {username}.txt", "w", encoding="utf-8") as f:
                    f.write(info)

                with open(f"./info/tokens/TOKEN_INFO {username}.txt", "rb") as f:
                    await ctx.send(content=f"```yaml\n{info}```", file=discord.File(f))

            except Exception as e:
                await ctx.send(f"""```yaml\n- Error: {e}```""", delete_after=5)

        await msg.delete(delay=5)

    @vbot.command(
        name="backup-f",
        description="Backups all of your friends (add true to send the txt file)",
        aliases=alias.get_aliases("backup-f")
    )
    async def _backup_f_(self, ctx: vbot.Context, send_txt: str = "false"):
        msg = ctx.message

        friends = ""

        for friend in self.bot.friends:
            friends += f"\n{friend.user.name}#{friend.user.discriminator} | {friend.user.id}"

        count = len(friends.splitlines())

        with open(f"./info/friends/{count} Friends.txt", "w", encoding="utf-8") as f:
            f.write(friends)
            print(
                f"{Fore.LIGHTGREEN_EX}+{Fore.RESET} Successfully saved {count} friends")
            await msg.edit(content=f"```yaml\n+ Successfully saved {count} friends```", delete_after=5)

        if send_txt == "true":
            with open(f"./info/friends/{count} Friends.txt", "rb") as f:
                await ctx.send(file=discord.File(f))

    @vbot.command(
        name="hypesquad",
        description="Changes your hypesquad. All hypesquads: bravery, brilliance, balance (put remove or delete to remove your hypesquad)"
    )
    # taken from zeenode (https://github.com/zeenode/selfbot/blob/master/zeenode/zeenode/cogs/main.py#L33) and slightly edited
    async def hypesquad(self, ctx: vbot.Context, house: str):
        msg = ctx.message
        headers = req.headers(main.token)
        house = house.lower()

        if house == "bravery":
            payload = {
                "house_id": 1
            }

        elif house == "brilliance":
            payload = {
                "house_id": 2
            }

        elif house == "balance":
            payload = {
                "house_id": 3
            }

        elif house == "remove" or house == "delete":
            payload = {}

        if payload != {}:
            async with aiohttp.ClientSession() as http:
                try:
                    await http.post(
                        f"{__api__}/hypesquad/online",
                        headers=headers,
                        json=payload)
                    return await msg.edit(content=f"```yaml\n+ Succesfully set hypesquad to {house}```", delete_after=5)

                except Exception as e:
                    return await msg.edit(content=f"```yaml\n- Couldn't set hypesquad to {house}. Error: {e}```", delete_after=5)

        else:
            async with aiohttp.ClientSession() as http:
                try:
                    await http.delete(
                        f"{__api__}/hypesquad/online",
                        headers=headers
                    )
                    return await msg.edit(content=f"```yaml\n+ Succesfully removed hypesquad```", delete_after=5)

                except Exception as e:
                    return await msg.edit(content=f"```yaml\n- Couldn't remove hypesquad. Error: {e}```", delete_after=5)

    @vbot.command(
        name="channelclear",
        description="Fully clears a channel"
    )
    async def channelclear(self, ctx: vbot.Context, channel=Optional[discord.TextChannel]):
        msg = ctx.message

        channel = channel or ctx.channel
        guild = channel.guild

        try:
            w_names = [w.name for w in await channel.webhooks()]

            await channel.delete()
            chann = await guild.create_text_channel(
                name=channel.name,
                overwrites=channel.overwrites,
                slowmode_delay=channel.slowmode_delay,
                position=channel.position,
                category=channel.category,
                topic=channel.topic
            )

            await asyncio.sleep(0.5)

            for w_name in w_names:
                await chann.create_webhook(name=w_name)

            await chann.edit(nsfw=channel.is_nsfw)

            sys_channel = channel == guild.system_channel
            if sys_channel == True:
                await guild.edit(system_channel=chann)

        except Exception as e:
            return await msg.edit(content=f"```yaml\n- An error has occurred: {e}```", delete_after=5)

    @vbot.command(
        name="discrim",
        description="Sends all the people with your tag"
    )
    async def discrim(self, ctx: vbot.Context):
        msg = ctx.message

        all = []
        for u in self.bot.users:
            if u.discriminator == self.bot.user.discriminator:
                all.append(
                    f"{u.name}#{u.discriminator}") if u != self.bot.user else None

        if all == []:
            all = "None"

        nl = "\n"

        await msg.edit(content=f"""```yaml
Found {len(all) if all != None else 0} people with the same tag:
{nl.join(all) if all != None else all}```""")

    @vbot.command(
        name="geoip",
        description="Sends information about an IP Address"
    )
    async def geoip(self, ctx: vbot.Context, ip: str):
        msg = ctx.message

        await msg.edit(content="```yaml\nGathering info...```")

        try:
            async with aiohttp.ClientSession() as http:
                r = await http.get(f"http://ip-api.com/json/{ip}?fields=12067839")
                r_2 = await http.get(f"https://ipapi.co/{ip}/json/")
                r_3 = await http.get(
                    f"https://ipinfo.io/widget/demo/{ip}",
                    headers={
                        "Accept": "*/*",
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Alt-Used": "ipinfo.io",
                        "Connection": "keep-alive",
                        "Content-Type": "application/json",
                        "Host": "ipinfo.io",
                        "Referer": "https://ipinfo.io/",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-origin",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 9; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4641.79 Mobile Safari/537.36"
                    })
                r_4 = await http.get(f"https://ipapi.com/ip_api.php?ip={ip}")

                ip1 = await r.json()
                ip2 = await r_2.json()
                ip3 = await r_3.json()
                ip4 = await r_4.json()
                data = {**ip1, **ip2, **ip3}
            try:
                hostname = data["data"]["hostname"]
            except KeyError:
                hostname = None

            emoji = flag.flag(data["countryCode"])
            c_symbol = ip4["currency"]["symbol"].encode("ascii").decode("unicode-escape").encode("utf-16", "surrogatepass").decode("utf-16")
            
            await msg.edit(content=f"""```yaml
IP Address: {data["query"]}
Hostname: {hostname}
Country: 
  - Name: {ip4["country_name"]}
  - Country Code: {data["countryCode"]}
  - Country Calling Code: {data["country_calling_code"]}
  - Country Emoji: {emoji} ({ip4["location"]["country_flag_emoji_unicode"]})
  - Is in EU: {ip4["location"]["is_eu"]}
  - Capital: {ip4["location"]["capital"]}
  - Currency: {ip4["currency"]["code"]} ({ip4["currency"]["name"]} / {c_symbol})
  - Continent: {data["continent"]}
  - Continent Code: {data["continentCode"]}

Timezone:
  - Timezone: {data["timezone"]}
  - Current Time: {ip4["time_zone"]["current_time"]}
  - GMT Offset: {ip4["time_zone"]["gmt_offset"]}
  - Code: {ip4["time_zone"]["code"]}
  - Is Daylight Saving: {ip4["time_zone"]["is_daylight_saving"]}

Location: 
  - Region: {data["regionName"]}
  - Region Code: {ip4["region_code"]}
  - City: {data["city"]}
  - ZIP Code: {data["zip"]}
  - Coordinates (lat long): {data["lat"]} {data["lon"]}

ISP: 
  - Name: {data["data"]["asn"]["name"]}
  - ASN: {data["data"]["asn"]["asn"]}
  - Domain: {data["data"]["asn"]["domain"]}
  - Route: {data["data"]["asn"]["route"]}
  - Address: {data["data"]["abuse"]["address"]}
  
Security:
  - VPN: {data["data"]["privacy"]["vpn"]}
  - Proxy: {data["data"]["privacy"]["proxy"]}
  - Tor: {data["data"]["privacy"]["tor"]}
  - Threat Level: {ip4["security"]["threat_level"].capitalize()}```
""")

        except KeyError as e:
            return await msg.edit(content=f"```yaml\n- Invalid IP Address: {e}```", delete_after=5)

        except Exception as e:
            return await msg.edit(content=f"```yaml\n- An unknown error occurred while gathering IP Address information: {e}```", delete_after=5)

    @vbot.command(
        name="pfp",
        description="Sets your pfp to a specified image link"
    )
    async def pfp(self, ctx: vbot.Context, *, img_url: str):
        msg = ctx.message

        try:
            async with aiohttp.ClientSession() as http:
                img = await http.get(img_url)
                img = await img.content()

                await self.bot.user.edit(avatar=img)
                await msg.edit(content=f"```yaml\n+ Succesfully set pfp to {img_url}```", delete_after=5)

        except Exception as e:
            await msg.edit(content=f"```yaml\n- An unknown error occurred: {e}```", delete_after=5)

    @vbot.command(
        name="log",
        description="Saves an amount of messages in the specified channel or the current channel"
    )
    async def log(self, ctx: vbot.Context, amount: int, channel_id: Optional[int]):
        msg = ctx.message
        fullstr = ""
        channel_id = channel_id or ctx.channel.id

        try:
            channel = self.bot.get_channel(channel_id)

        except Exception as e:
            return await msg.edit(content=f"```yaml\nAn error has occurred while trying to find the specified channel: {e}```", delete_after=5)

        await msg.edit(content=f"```yaml\nSaving {amount} messsages...```")

        msgs = [msg async for msg in channel.history(limit=amount)]
        msgs.reverse()
        count = 0

        for msg in msgs:
            author = msg.author
            date = msg.created_at
            content = msg.content
            channel = ctx.channel
            atts = [att.url for att in msg.attachments]
            nl = "\n"

            try:
                reply = await msg.channel.fetch_message(msg.reference.message_id)
            except:
                reply = ""

            message = f"""
  {author} | {date}
  - {content}{f"{nl}  - Attachments: {', '.join(atts)}" if msg.attachments else ""}
  {f"- Replying to: {reply.author}" if reply != "" else ""}\n"""
            fullstr += message
            count += 1

        with open(f"./info/logs/LOG_INFO #{channel} {count}.txt", "w", encoding="utf-8") as f:
            f.write(fullstr)

        with open(f"./info/logs/LOG_INFO #{channel} {count}.txt", "rb") as f:
            await msg.delete()
            await ctx.send(f"```yaml\n+ Succesfully saved {count} messages```", file=discord.File(f))

    @vbot.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        try:
            self.snipe_message[message.channel.id] = message
            await asyncio.sleep(120)
            del self.snipe_message[message.channel.id]

        except:
            pass

    @vbot.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        try:
            self.snipe_message_edit[before.channel.id] = {
                "before": before,
                "after": after
            }
            await asyncio.sleep(120)
            del self.snipe_message_edit[before.channel.id]

        except:
            pass

    @vbot.group(
        name="snipe",
        description="For all the normies with no message logger",
        invoke_without_command=True
    )
    async def snipe(self, ctx: vbot.Context):
        msg = ctx.message
        channel = ctx.channel
        try:
            message = self.snipe_message[channel.id]
            clean = message.content.replace("`", "")
            await msg.edit(content=f"```yaml\n- {message.author} | {message.created_at}\n   {clean}```")

        except KeyError:
            await msg.edit(content=f"```yaml\nThere have been no recently deleted messages in the past 2 minutes.```")

    @snipe.command(
        name="edit",
        description="Snipes edited messages",
        invoke_without_command=True
    )
    async def edit(self, ctx: vbot.Context):
        msg = ctx.message
        channel = ctx.channel

        try:
            obj = self.snipe_message_edit[channel.id]
            before = obj["before"]
            after = obj["after"]

            clean_b = before.content.replace("`", "")
            clean_a = after.content.replace("`", "")

            await msg.edit(content=f"```yaml\n- {before.author} | {before.created_at}\n   Original: {clean_b}\n   Edited: {clean_a}```")

        except KeyError:
            await msg.edit(content=f"```yaml\nThere have been no recently edited messages in the past 2 minutes.```")

    @vbot.command(
        name="prefixes",
        description="Sends a list of all the prefixes"
    )
    async def prefixes(self, ctx: vbot.Context):
        pfxs = main.prefix
        msg = ctx.message
        nl = "\n- "

        await msg.edit(content=f"```yaml\nThere are/is {len(pfxs)} prefix(es):\n- {nl.join(pfxs)}```", delete_after=5)

    @vbot.command(
        name="readserver",
        description="Marks all the channels in a server as read"
    )
    async def readserver(self, ctx: vbot.Context, server_id: Optional[int]):
        server_id = server_id or ctx.guild.id
        msg = ctx.message

        try:
            guild: discord.Guild = self.bot.get_guild(server_id)
            await guild.ack()
            await msg.edit(content=f"```yaml\n+ Succesfully marked as read all channels in {guild.name}```", delete_after=5)

        except:
            return await ctx.send("```yaml\n- Error: Invalid server ID```", delete_after=5)

    @tasks.loop(hours=2)
    async def autobump(self):
        if self.bump["bumping"] and self.bump["cmd_obj"]:
            await self.bump["cmd_obj"].__call__()

    @vbot.command(
        name="abump",
        description="Starts or stops auto disboard bump in the selected channel"
    )
    async def abump(self, ctx: vbot.Context, channel: Optional[discord.TextChannel]):
        msg = ctx.message
        channel: discord.TextChannel = channel or ctx.channel

        if not isinstance(channel, discord.TextChannel):
            return await msg.edit(content="```yaml\n- Channel cannot be a DM.```", delete_after=5)

        try:
            disboard = await channel.guild.fetch_member(302050872383242240)

        except discord.NotFound:
            return await msg.edit(content="```yaml\n- DISBOARD is not in the server.```", delete_after=5)

        found = False
        async for cmd in channel.slash_commands():
            if cmd.application_id == disboard.id:
                found = True
                if cmd.name == "bump":
                    self.bump["bumping"] = not self.bump["bumping"]
                    if self.bump["bumping"] == False:
                        await msg.edit(content="```yaml\n- Canceled autobump task.```", delete_after=5)
                        await self.autobump.cancel()

                    else:
                        await msg.edit(content="```yaml\n+ Started autobump task.```", delete_after=5)
                        self.bump["cmd_obj"] = cmd
                        await self.autobump.start()

        if not found:
            await msg.edit(content="```yaml\n- DISBOARD can't be accessed in the selected channel.```", delete_after=5)


if __name__ == "__main__":
    print("You need to run main.py to run the bot")


async def setup(bot):
    await bot.add_cog(UtilityCmds(bot))
