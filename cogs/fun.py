import selfcord as discord
import random
import base64
import secrets
import string
import aiohttp
import json
import io
import socket
import struct
import main
from selfcord.ext import commands as vbot
from utils import alias


class FunCmds(
        vbot.Cog,
        name="Fun",
        description="Various fun commands"):
    def __init__(self, bot: vbot.Bot):
        self.bot = bot
        self.copy_ids = []

    @vbot.group(
        name="copycat",
        description="Copies messages sent by an user.",
        invoke_without_command=True,
        aliases=alias.get_aliases("copycat")
    )
    async def copycat(self, ctx: vbot.Context, user: discord.User):
        msg = ctx.message

        if user.id in self.copy_ids:
            return await msg.edit("```yaml\n- Already copying that user.```", delete_after=5)

        if ctx.message.author.id == user.id:
            return await msg.edit("```yaml\n- You can\'t copy yourself.```", delete_after=5)

        self.copy_ids.append(user.id)
        await msg.edit(content=f"```yaml\n+ Now copying {user}```", delete_after=5)

    @copycat.command(
        name="reset",
        description="Resets copycat"
    )
    async def reset(self, ctx: vbot.Context):
        self.copy_ids = []
        await ctx.message.edit(content="```yaml\n+ Succesfully reset copycat list.```", delete_after=5)

    @vbot.command(
        name="someone",
        description="Pings a random person in a server (if it doesn't work don't blame me)"
    )
    async def someone(self, ctx: vbot.Context):
        msg = ctx.message
        guild = ctx.guild
        members = [member.mention for member in guild.members]

        await msg.edit(content=secrets.choice(members))

    @vbot.command(
        name="stealpfp",
        description="Steals someones pfp (after 2 - 3 pfps there will be a ratelimit)",
        aliases=alias.get_aliases("stealpfp")
    )
    async def stealpfp(self, ctx: vbot.Context, member: discord.User):
        msg = ctx.message

        avatar_url = str(member.avatar.url)

        try:
            async with aiohttp.ClientSession() as http:
                img = await http.get(avatar_url)
                img = await img.content.read()

            await self.bot.user.edit(avatar=img)
            await msg.edit(content=f"```yaml\n+ Succesfully set pfp to {member}'s profile picture```", delete_after=5)

        except Exception as e:
            await msg.edit(content=f"```yaml\n- An unknown error occurred: {e}```", delete_after=5)

    @vbot.command(
        name="tokengrab",
        description="ACTUALLY token grabs someone. Do not use this in public!!",
        aliases=alias.get_aliases("tokengrab")
    )
    async def tokengrab(self, ctx: vbot.Context, member: discord.User):
        with open("./fun/tokens.json") as json_f:
            data = json.load(json_f)

        msg = ctx.message
        mid = str(member.id)

        if mid not in data:
            id_ascii = mid.encode("ascii")
            id_base64 = base64.b64encode(id_ascii)
            id_idk = id_base64.decode("ascii")
            timest = "".join(random.choices(
                string.ascii_letters + string.digits + "-" + "_", k=6))
            last = "".join(random.choices(
                string.ascii_letters + string.digits + "-" + "_", k=27))
            await msg.edit(content=f"```yaml\n+ Succesfully token grabbed {member}.\nToken: {id_idk}.{timest}.{last}```")
            data[mid] = f"{id_idk}.{timest}.{last}"

            with open("./fun/tokens.json", "w") as out:
                json.dump(data, out, indent=4)

        else:
            token = data[mid]
            await msg.edit(content=f"```yaml\n+ Succesfully token grabbed {member}.\nToken: {token}```")

    @vbot.command(
        name="ip",
        description="ACTUALLY ip grabs someone. Do not use this in public!!",
        aliases=alias.get_aliases("ip")
    )
    async def ip(self, ctx: vbot.Context, member: discord.User):
        with open("./fun/ips.json") as json_f:
            data = json.load(json_f)

        msg = ctx.message
        mid = str(member.id)

        if mid not in data:
            rand_ip = socket.inet_ntoa(struct.pack(
                ">I", random.randint(1, 0xffffffff)))
            await msg.edit(content=f"```yaml\n+ Succesfully IP grabbed {member}.\nIP Address: {rand_ip}```")
            data[mid] = rand_ip

            with open("./fun/ips.json", "w") as out:
                json.dump(data, out, indent=4)

        else:
            ip = data[mid]
            await msg.edit(content=f"```yaml\n+ Succesfully IP grabbed {member}.\nIP Address: {ip}```")

    @vbot.group(
        name="gen",
        description="Various commands to generate fake info",
        aliases=alias.get_aliases("gen"),
        invoke_without_command=True
    )
    async def gen(self, ctx: vbot.Context):
        await ctx.message.delete()

    @gen.command(
        name="tokens",
        description="Generates tokens",
        aliases=["token"]
    )
    async def tokens(self, ctx: vbot.Context, amount: int = 20):
        msg = ctx.message
        tokens = []

        for _ in range(amount):
            id_ascii = str(secrets.choice(
                range(650000000000000000, 1200000000000000000))).encode("ascii")
            id_base64 = base64.b64encode(id_ascii)
            id_idk = id_base64.decode("ascii")
            timest = "".join(random.choices(
                string.ascii_letters + string.digits + "-" + "_", k=6))
            last = "".join(random.choices(
                string.ascii_letters + string.digits + "-" + "_", k=27))
            token = f"{id_idk}.{timest}.{last}"
            tokens.append(token)

        nl = "\n"
        fullstr = f"""Generated {amount} tokens
{nl.join(tokens)}"""
        if len(fullstr) > 1998:
            await msg.edit(content="```yaml\nMaking txt file...```")
            f = io.StringIO(fullstr)
            await ctx.send(file=discord.File(f, filename="tokens.txt"))
            await msg.delete()

        else:
            await msg.edit(content=f"""```yaml
Generated {amount} tokens
{nl.join(tokens)}```""")

    @gen.command(
        name="ips",
        description="Generates IPs",
        aliases=["ip"]
    )
    async def ips(self, ctx: vbot.Context, amount: int = 20):
        msg = ctx.message
        ips = []

        for _ in range(amount):
            ip = socket.inet_ntoa(struct.pack(
                ">I", random.randint(1, 0xffffffff)))
            ips.append(str(ip))

        nl = "\n"
        fullstr = f"""Generated {amount} IPs
{nl.join(ips)}"""
        if len(fullstr) > 1998:
            await msg.edit(content="```yaml\nMaking txt file...```")
            f = io.StringIO(fullstr)
            await ctx.send(file=discord.File(f, filename="ips.txt"))
            await msg.delete()

        else:
            await msg.edit(content=f"""```yaml
Generated {amount} IPs
{nl.join(ips)}```""")

    @gen.command(
        name="ids",
        description="Generates Discord IDs",
        aliases=["id"]
    )
    async def ids(self, ctx: vbot.Context, amount: int = 20):
        msg = ctx.message
        ids = []

        for _ in range(amount):
            id = str(secrets.choice(
                range(100000000000000000, 1200000000000000000)))
            ids.append(id)

        nl = "\n"
        fullstr = f"""Generated {amount} IDs
{nl.join(ids)}"""
        if len(fullstr) > 1998:
            await msg.edit(content="```yaml\nMaking txt file...```")
            f = io.StringIO(fullstr)
            await ctx.send(file=discord.File(f, filename="ids.txt"))
            await msg.delete()

        else:
            await msg.edit(content=f"""```yaml
Generated {amount} IDs
{nl.join(ids)}```""")

    @gen.command(
        name="nitro",
        description="Generates Discord nitro codes"
    )
    async def nitro(self, ctx: vbot.Context, amount: int = 20):
        msg = ctx.message
        codes = []

        for _ in range(amount):
            code = "".join(random.choices(
                string.ascii_letters + string.digits, k=16))
            codes.append(f"https://discord.gift/{code}")

        nl = "\n"
        fullstr = f"""Generated {amount} nitro code(s)
{nl.join(codes)}"""
        if len(fullstr) > 1998:
            await msg.edit(content="```yaml\nMaking txt file...```")
            f = io.StringIO(fullstr)
            await ctx.send(file=discord.File(f, filename="nitro_codes.txt"))
            await msg.delete()

        else:
            await msg.edit(content=f"""```yaml
Generated {amount} nitro code(s)
{nl.join(codes)}```""")
    
    @gen.command(
        name="invites",
        description="Generates Discord invites",
        aliases=["invite"]
    )
    async def invites(self, ctx: vbot.Context, amount: int = 20):
        msg = ctx.message
        codes = []

        for _ in range(amount):
            code = "".join(random.choices(
                string.ascii_letters + string.digits, k=random.choice([8, 10])))
            codes.append(f"https://discord.gg/{code}")

        nl = "\n"
        fullstr = f"""Generated {amount} invite code(s)
{nl.join(codes)}"""
        if len(fullstr) > 1998:
            await msg.edit(content="```yaml\nMaking txt file...```")
            f = io.StringIO(fullstr)
            await ctx.send(file=discord.File(f, filename="invite_codes.txt"))
            await msg.delete()

        else:
            await msg.edit(content=f"""```yaml
Generated {amount} invite code(s)
{nl.join(codes)}```""")

    @vbot.command(
        name="firstmsg",
        description="Sends the first message in the current channel"
    )
    async def firstmsg(self, ctx: vbot.Context):
        msg = ctx.message
        channel = ctx.channel

        history = [msg async for msg in channel.history(limit=1, oldest_first=True)]
        firstm = history[0]
        await msg.edit(content=f"""```yaml
From: {firstm.author}
Message: {firstm.content.replace("`", "")}

Message URL: {firstm.jump_url}```""")

    @vbot.group(
        name="fact",
        description="A bunch of animal facts",
        invoke_without_command=True
    )
    async def facts(self, ctx: vbot.Context):
        msg = ctx.message
        await msg.edit(content=f"```yaml\n- Incorrect usage. Correct usage: {ctx.clean_prefix}help [facts]```", delete_after=5)

    @facts.command(
        name="bird",
        description="Random bird fact"
    )
    async def bird(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/bird")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nBird Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @facts.command(
        name="cat",
        description="Random cat fact"
    )
    async def cat(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/cat")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nCat Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @facts.command(
        name="dog",
        description="Random dog fact"
    )
    async def dog(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/dog")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nDog Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @facts.command(
        name="kangaroo",
        description="Random kangaroo fact"
    )
    async def kangaroo(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/kangaroo")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nKangaroo Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @facts.command(
        name="raccoon",
        description="Random raccoon fact"
    )
    async def raccoon(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/raccoon")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nRaccoon Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @facts.command(
        name="panda",
        description="Random panda fact"
    )
    async def panda(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/panda")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nPanda Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @facts.command(
        name="fox",
        description="Random fox fact"
    )
    async def fox(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/fox")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nFox Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @facts.command(
        name="koala",
        description="Random koala fact"
    )
    async def koala(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/koala")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nKoala Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @facts.command(
        name="redpanda",
        description="Random red panda fact"
    )
    async def redpanda(self, ctx: vbot.Context):
        msg = ctx.message

        async with aiohttp.ClientSession() as http:
            r = await http.get(f"https://some-random-api.ml/animal/red_panda")
            js = await r.json()
            fact = js["fact"]
            image = js["image"]
            await ctx.send(f"""```yaml\nRed Panda Fact: {fact}```\n{image}""")

        await msg.delete(delay=5)

    @vbot.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id in self.copy_ids:
            if message.content.startswith(tuple(main.prefix)):
                return
            else:
                await message.channel.send(message.content)


if __name__ == "__main__":
    print("You need to run main.py to run the bot")


async def setup(bot):
    await bot.add_cog(FunCmds(bot))
