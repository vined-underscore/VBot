import datetime
import selfcord as discord
import main
import asyncio
import aiosonic
from selfcord.ext import commands as vbot
from colorama import Fore
from utils import req
from utils import alias
from utils.req import __api__
from utils.msg import delete_msg
from datetime import datetime
from typing import Optional

class UtilityCmds(
    vbot.Cog,
    name = "Utils",
    description = "Various useful commands"):
  def __init__(self, bot):
    self.bot = bot
    self.is_clear = False
    self.snipe_message = {}
    self.snipe_message_edit = {}
    self.msgs = 0
    self.deleted = 0
    self.messages = []

  @vbot.group(
    name = "clear",
    description = "Clears messages. Put an ID to specifically clear a channel",
    aliases = alias.get_aliases("clear"),
    invoke_without_command = True
  )
  async def clear(self, ctx, amount: int, channel_id: int = None):
    self.is_clear = True
    
    msg = ctx.message
      
    if channel_id is not None:
        channel = self.bot.get_channel(channel_id)

    else:
        channel = msg.channel

    if isinstance(channel, discord.GroupChannel) or isinstance(channel, discord.DMChannel):
      count = 0
      async for message in channel.history(limit = amount):  
          if self.is_clear == False: return
          if not message.author == self.bot.user: continue
          if message == msg: continue

          try:
            await message.delete()
            count += 1

          except:
            pass
          
      await msg.edit(content = f"```yaml\n+ Deleted {count} messages.```", delete_after = 5)

    else:
      def purge(m):
        return m.author == self.bot.user and m != msg
      
      deleted = await channel.purge(limit = amount, check = purge)

      self.is_clear = False
      await msg.edit(content = f"```yaml\n+ Deleted {len(deleted)} messages.```", delete_after = 5)

  @clear.command(
    name = "antireport",
    description = "Deletes all messages by you in every server/dm that contain a specific string (Might take a while)",
    aliases = alias.get_aliases("antireport")
  )
  async def antireport(self, ctx, *, messg):
    msg = ctx.message
    
    await msg.edit(content = f"""```yaml\nStarting purge process...```""")
    print(f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Starting antireport purge...\n")

    async def search_guild(self, guild):
      print(f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Moving over to server {Fore.LIGHTBLUE_EX}{guild.name}{Fore.LIGHTWHITE_EX}\n")
      
      if guild.member_count > 500:
        print(f"{Fore.RED}[-]{Fore.LIGHTWHITE_EX} {Fore.LIGHTBLUE_EX}{guild.name}{Fore.LIGHTWHITE_EX} has more than 500 members, skipping...\n")
        return
      
      for channel in guild.text_channels:
        print(f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Looking through {Fore.LIGHTBLUE_EX}#{channel.name}{Fore.LIGHTWHITE_EX} in {Fore.LIGHTBLUE_EX}{guild.name}{Fore.LIGHTWHITE_EX}... ({self.msgs} messages so far)")
        
        if not channel.permissions_for(guild.me).send_messages:
          print(f"{Fore.RED}[-]{Fore.LIGHTWHITE_EX} User doesn't have message access in {Fore.LIGHTBLUE_EX}#{channel.name}{Fore.LIGHTWHITE_EX}, skipping...\n")
          continue
        
        try:
          async for message in channel.history(limit = None):
            self.msgs += 1
            if message.author == self.bot.user:
              if messg.lower() in message.content.lower():
                self.messages.append(message)
                print(f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Found message with string \"{messg}\" in {Fore.LIGHTBLUE_EX}#{channel.name}{Fore.LIGHTWHITE_EX}")
                await message.delete()
                self.deleted += 1
                await asyncio.sleep(1)
                
        except discord.Forbidden:
          print(f"{Fore.RED}[-]{Fore.LIGHTWHITE_EX} User doesn't have access in {Fore.LIGHTBLUE_EX}#{channel.name}{Fore.LIGHTWHITE_EX}, skipping...\n")
          await asyncio.sleep(1)
          continue
          
        except discord.HTTPException:
          await asyncio.sleep(5)
        
        await asyncio.sleep(5)
        
    coros = [search_guild(self, guild) for guild in self.bot.guilds]
    await asyncio.gather(*coros)
    
    await msg.edit(content = f"""```yaml\nSuccesfully deleted {self.deleted}/{len(self.messages)} messages.```""", delete_after = 15)
    self.msgs = 0
    self.deleted = 0
    self.messages = []
      
  @clear.command(
    name = "stop",
    description = "Stops the clear command"
  )
  async def stop(self, ctx):
    msg = ctx.message
    
    if self.is_clear == False:
        await msg.edit(content = "```yaml\n- There is no clear going on``", delete_after = 5)

    else:
        self.is_clear = False
        await msg.edit(content = "```yaml\n+ Stopped clear```", delete_after = 5)

  @vbot.command(
    name = "msgedit",
    description = "Edits an amount of your messages in the channel"
  )
  async def msgedit(self, ctx, amount: int, *, txt: str):
    msg = ctx.message
    channel = ctx.channel
    await delete_msg(msg)
    history = [m async for m in channel.history(limit=amount)]

    for message in history:
      if message.author == self.bot.user:
        await message.edit(content=txt)

  @vbot.group(
    name = "info",
    description = "Various commands to show information about things",
    invoke_without_command = True
  )
  async def info(self, ctx):
    msg = ctx.message
    await msg.edit(content=f"```yaml\n- Incorrect usage. Correct usage: {main.prefix}help [info]```", delete_after = 5)

  @info.command(
    name = "user",
    description = "Saves user info of an user to the info folder (may not work if user has some non ascii characters in their name)",
    aliases = alias.get_aliases("user")
  )
  async def user(self, ctx, user: discord.User = None):
    msg = ctx.message
    if not user:
      user = msg.author

    await delete_msg(msg)

    invalid_chars = "#%&{}\<>*?/ $!'\":@+`|="
    username = str(user)
    for char in invalid_chars:
      if char in username:
        username = username.replace(char, "_")
    
    with open(f"./info/users/USER_INFO {username}.txt", "w") as f:
      req = await self.bot.http.request(
        discord.http.Route(
          "GET",
          "/users/{uid}",
          uid = user.id))
      
      banner_id = req["banner"]
      if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
        
      else:
        pass

      now = datetime.now().astimezone()
      created_at = user.created_at
      days_ago = now - created_at
      
      f.write(f"""
Username: {user.name}#{user.discriminator}
User ID: {user.id}
Created at: {created_at.strftime("%b %d %Y")} ({days_ago.days} days ago)
Avatar url: {user.avatar.url}
Banner url: {banner_url if banner_id else "None"}
Is a bot: {user.bot}
""")
    with open(f"./info/users/USER_INFO {username}.txt", "rb") as f:
      await ctx.send(file=discord.File(f))
  
  @info.command(
    name = "server",
    description = "Saves server info of the current server (or by id) to the info folder (may not work if server has some non ascii characters in its name)",
    aliases = alias.get_aliases("server")
  )
  async def server(self, ctx, server_id: int = None):
    msg = ctx.message
    
    await delete_msg(msg)
    if not server_id:
      guild = ctx.guild

    else:
      try:
        guild = self.bot.get_guild(server_id)
    
      except:
        return await ctx.send("```yaml\n- Error: Invalid server ID```", delete_after = 5)

    invalid_chars = "#%&{}\<>*?/ $!'\":@+`|="
    servername = str(guild.name)
    for char in invalid_chars:
      if char in servername:
        servername = servername.replace(char, "_")

    try:
      channel = guild.text_channels[0]
      invite = await channel.create_invite(max_age = 0, max_uses = 0)
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
    
    with open(f"./info/servers/SERVER_INFO {servername}.txt", "w") as f:
      now = datetime.now().astimezone()
      created_at_server = guild.created_at
      days_ago_server = now - created_at_server
      created_at_owner = owner.created_at
      days_ago_owner = now - created_at_owner
      
      f.write(f"""
Server name: {guild.name}
Server ID: {guild.id}
Amount of text channels: {text_channels}
Amount of voice channels: {voice_channels}
Amount of categories: {categories}
Amount of all channels: {all_channels}
Amount of roles: {roles}
Amount of emojis: {emojis}
Amount of members: {members}
Created at: {created_at_server.strftime("%b %d %Y")} ({days_ago_server.days} days ago)
Icon url: {guild.icon}
Invite: {invite}

Owner information:
  Name: {owner.name}#{owner.discriminator}
  ID: {owner.id}
  Created at: {created_at_owner.strftime("%b %d %Y")} ({days_ago_owner.days} days ago)
  Avatar url: {owner.avatar.url}
  Banner url: {banner_url if banner_id else "None"}
  Is a bot: {owner.bot}
""")
    with open(f"./info/servers/SERVER_INFO {servername}.txt", "rb") as f:
      await ctx.send(file=discord.File(f))

  @info.command(
    name = "token",
    description = "Gets information from a token (may not work if token has some non ascii characters in its name)"
  )
  async def token(self, ctx, token):
    msg = ctx.message
    
    async with aiosonic.HTTPClient() as http:
      r_user = await http.get(
        "https://discord.com/api/v9/users/@me",
        headers = {
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
          n = nitro_types[str(js['premium_type'])]

        except Exception as e:
          n = "None"
          
        invalid_chars = "#%&{}\<>*?/ $!'\":@+`|="
        username = f"{js['username']}#{str(js['discriminator'])}"
        for char in invalid_chars:
          if char in username:
            username = username.replace(char, "_")

        info = f"""Token: {token}
Username: {js['username']}#{js['discriminator']}
ID: {js['id']}
Email: {js['email']}
Phone: {js['phone']}
Avatar URL: https://cdn.discordapp.com/avatars/{js['id']}/{js['avatar']}.png?size=2048
Banner URL: https://cdn.discordapp.com/banners/{js['id']}/{js['banner']}.png?size=2048
Bio: {None if js['bio'] == '' else js['bio']}
Locale: {js['locale']}
2FA Enabled: {js['mfa_enabled']}
Verified: {js['verified']}
Nitro Subscription: {n}"""

        with open(f"./info/tokens/TOKEN_INFO {username}.txt", "w") as f:
          f.write(info)
        
        with open(f"./info/tokens/TOKEN_INFO {username}.txt", "rb") as f:
          await ctx.send(file=discord.File(f))
    
      except Exception as e:
        await ctx.send(f"""```yaml
  - {e}
  ```""", delete_after = 5)
    
    await delete_msg(msg)

  @vbot.command(
    name = "backup-f",
    description = "Backups all of your friends (add true to send the txt file)",
    aliases = alias.get_aliases("backup-f")
  )
  async def _backup_f_(self, ctx, send_txt = "false"):
    msg = ctx.message
    
    friends = ""
    
    for friend in self.bot.friends:
      friends += f"\n{friend.user.name}#{friend.user.discriminator} | {friend.user.id}"
      
    count = len(friends.splitlines())
      
    with open(f"./info/friends/{count} Friends.txt", "w", encoding="utf-8") as f:
      f.write(friends)
      print(f"{Fore.LIGHTGREEN_EX}+{Fore.RESET} Successfully saved {count} friends")
      await msg.edit(content = f"```yaml\n+ Successfully saved {count} friends```", delete_after = 5)
      
    if send_txt == "true":
      with open(f"./info/friends/{count} Friends.txt", "rb") as f:
        await ctx.send(file=discord.File(f))

  @vbot.command(
    name = "hypesquad",
    description = "Changes your hypesquad. All hypesquads: bravery, brilliance, balance (put remove or delete to remove your hypesquad)"
  )
  #taken from zeenode (https://github.com/zeenode/selfbot/blob/master/zeenode/zeenode/cogs/main.py#L33) and slightly edited
  async def hypesquad(self, ctx, house):
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
      async with aiosonic.HTTPClient() as http:
        try:
          await http.post(
            f'{__api__}/hypesquad/online',
            headers = headers,
            json = payload)
          return await msg.edit(content = f"```yaml\n+ Succesfully set hypesquad to {house}```", delete_after = 5)
      
        except Exception as e:
          return await msg.edit(content = f"```yaml\n- Couldn't set hypesquad to {house}. Error: {e}```", delete_after = 5)

    else:
      async with aiosonic.HTTPCLient() as http:
        try:
          await http.delete(
            f'{__api__}/hypesquad/online',
            headers = headers
          )
          return await msg.edit(content = f"```yaml\n+ Succesfully removed hypesquad```", delete_after = 5)
      
        except Exception as e:
          return await msg.edit(content = f"```yaml\n- Couldn't remove hypesquad. Error: {e}```", delete_after = 5)

  @vbot.command(
    name = "channelclear",
    description = "Fully clears a channel in an instant"
  )
  #made by me frfr
  async def channelclear(self, ctx, channel = Optional[discord.TextChannel]):
    msg = ctx.message

    channel = channel or ctx.channel
    guild = channel.guild   

    try:
      headers = req.headers(main.token)
      w_names = [w.name for w in await channel.webhooks()]

      pos = channel.position
      topic = channel.topic
      cat = channel.category
      name = channel.name
      perms = channel.overwrites
      slowmode = channel.slowmode_delay
      nsfw = channel.is_nsfw
      sys_channel = channel == guild.system_channel

      await channel.delete()
      chann = await guild.create_text_channel(
        name = name,
        overwrites = perms,
        slowmode_delay = slowmode,
        position = pos,
        category = cat,
        topic = topic
      )

      await asyncio.sleep(0.5)
      
      for w_name in w_names:
        await chann.create_webhook(name = w_name)
    
      await chann.edit(nsfw = nsfw)
      
      if sys_channel == True:
        async with aiosonic.HTTPClient() as http:
          await http.patch(
            f"{__api__}/guilds/{guild.id}",
            headers = headers,
            json = {
              "system_channel_id": chann.id
            })

    except Exception as e:
      return await msg.edit(content = f"```yaml\n- An error has occurred: {e}```", delete_after = 5)

  @vbot.command(
    name = "discrim",
    description = "Sends all the people with your tag"
  )
  async def discrim(self, ctx):
    msg = ctx.message
    
    all = []
    for u in self.bot.users:
      if u.discriminator == self.bot.user.discriminator:
          all.append(f"{u.name}#{u.discriminator}") if u != self.bot.user else None
    
    if all == []:
      all = "None"
      
    nl = "\n"
      
    await msg.edit(content = f"""```yaml
Found {len(all)} people with the same tag:
{nl.join(all)}```""")
    
  @vbot.command(
    name = "geoip",
    description = "Sends information about an IP Address"
  )
  async def geoip(self, ctx, query):
    msg = ctx.message
    
    await msg.edit(content = "Gathering info...")
    
    url = f"http://ip-api.com/json/{query}?fields=12067839"
    url_2 = f"https://ipapi.co/{query}/json/"
    
    try:
      async with aiosonic.HTTPClient() as http:
        r = await http.get(url)
        r_2 = await http.get(url_2)
        
        ip_json = await r.json()
        ip2_json = await r_2.json()
      
      await msg.edit(content = f"""```yaml
IP Address: {ip_json['query']}
ISP: {ip2_json['org']}
Country: {ip_json['country']}
Country Code: {ip_json['countryCode']}
Country Calling Code: {ip2_json['country_calling_code']}
Region: {ip_json['regionName']}
City: {ip_json['city']}
ZIP Code: {ip_json['zip']}
Latitude: {ip_json['lat']}
Longitude: {ip_json['lon']}
Continent: {ip_json['continent']}
Continent Code: {ip_json['continentCode']}
Timezone: {ip_json['timezone']}```
""")
      
    except KeyError:
      return await msg.edit(content = f"```yaml\n- An error occurred while gathering IP Address information: Invalid IP Address```", delete_after = 5)
    
    except Exception as e:
      return await msg.edit(content = f"```yaml\n- An unknown error occurred while gathering IP Address information: {e}```", delete_after = 5)
    
  @vbot.command(
    name = "pfp",
    description = "Sets your pfp to a specified image link"
  )
  async def pfp(self, ctx, *, img_url: str):
    msg = ctx.message
    
    try:
      async with aiosonic.HTTPClient() as http:
        img = await http.get(img_url)
        img = await img.content()

        await self.bot.user.edit(avatar=img)
        await msg.edit(content = f"```yaml\n+ Succesfully set pfp to {img_url}```", delete_after = 5)

    except Exception as e:
      await msg.edit(content = f"```yaml\n- An unknown error occurred: {e}```", delete_after = 5)
      
  @vbot.command(
    name = "log",
    description = "Puts an amount of messages in the specified channel or the current channel in a file."
  )
  async def log(self, ctx, amount: int, channel_id: int = None):
    msg = ctx.message
    fullstr = ""  
    
    if channel_id is None:
      channel = ctx.channel
    
    else:
      try:
        channel = self.bot.get_channel(channel_id)
      
      except Exception as e:
        return await msg.edit(content = f"```yaml\nAn error has occurred while trying to find the specified channel: {e}```", delete_after = 5)
    
    await msg.edit(content = f"```yaml\nSaving {amount} messsages...```")
    
    msgs = [msg async for msg in channel.history(limit = amount)]
    msgs.reverse()
    count = 0
    
    for msg in msgs:
      author = msg.author
      date = msg.created_at
      content = msg.content
      channel = ctx.channel
      
      message = f"""
  {author} | {date}
  - {content}\n"""
      fullstr += message
      count += 1
    
    with open(f"./info/logs/LOG_INFO #{channel} {count}.txt", "w", encoding="utf-8") as f:
      f.write(fullstr)
      await msg.delete()

    with open(f"./info/logs/LOG_INFO #{channel} {count}.txt", "rb") as f:
      await ctx.send(f"```yaml\n+ Succesfully saved {count} messages```", file=discord.File(f))
    

  @vbot.Cog.listener()
  async def on_message_delete(self, message):
    try:
      self.snipe_message[message.channel.id] = message
      await asyncio.sleep(60)
      del self.snipe_message[message.channel.id]
    
    except:
      pass
    
  @vbot.Cog.listener()
  async def on_message_edit(self, before, after):
    try:
      self.snipe_message_edit[before.channel.id] = {
        "before": before,
        "after": after
      }
      await asyncio.sleep(60)
      del self.snipe_message_edit[before.channel.id]
    
    except:
      pass
  
  @vbot.group(
    name = "snipe",
    description = "For all the normies with no message logger",
    invoke_without_command = True
  )
  async def snipe(self, ctx):
    msg = ctx.message
    channel = ctx.channel
    try:
      message = self.snipe_message[channel.id]
      clean = message.content.replace('`', '')
      await msg.edit(content = f"```yaml\n- {message.author} | {message.created_at}\n   {clean}```")
      
    except KeyError:
        await msg.edit(content = f"```yaml\nThere have been no recently deleted messages in the past minute.```")
        
  @snipe.command(
    name = "edit",
    description = "Snipes edited messages",
    invoke_without_command = True
  )
  async def edit(self, ctx):
    msg = ctx.message
    channel = ctx.channel
    
    try:
      obj = self.snipe_message_edit[channel.id]
      before = obj['before']
      after = obj['after']
  
      clean_b = before.content.replace('`', '')
      clean_a = after.content.replace('`', '')
      
      await msg.edit(content = f"```yaml\n- {before.author} | {before.created_at}\n   Original: {clean_b}\n   Edited: {clean_a}```")
      
    except KeyError:
        await msg.edit(content = f"```yaml\nThere have been no recently edited messages in the past minute.```")

  @vbot.command(
    name = "prefixes",
    description = "Sends a list of all the prefixes"
  )
  async def prefixes(self, ctx):
    pfxs = main.prefix
    msg = ctx.message
    nl = "\n- "
    
    await msg.edit(f"```yaml\nThere are/is {len(pfxs)} prefix(es):\n- {nl.join(pfxs)}```", delete_after = 5)
    
if __name__ == "__main__":
    print("You need to run main.py to run the bot")

async def setup(bot):
  await bot.add_cog(UtilityCmds(bot))
