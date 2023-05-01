import discord
import config
import aiohttp
from datetime import datetime
from colorama import Fore as F
from discord.ext import commands as vbot
from utils import other
from utils.other import log


class Events(
        vbot.Cog,
        name="Events"):
    def __init__(self, bot: vbot.Bot):
        self.bot = bot
        self.webhook = ""

    @vbot.Cog.listener()
    async def on_connect(self):
        await self.bot.full_banner()
        if config.logging["url"] == "":
            return

        async with aiohttp.ClientSession() as session:
            try:
                self.webhook = discord.Webhook.from_url(
                    config.logging["url"], session=session)
            except:
                print(
                    f"{F.RED}The webhook in the logging config is invalid. Change it to a valid webhook or blank to disable it.")
                exit()

    @vbot.Cog.listener()
    async def on_message(self, message: discord.Message):
        self.bot.total_msgs += 1

    @vbot.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        await self.bot.process_commands(after)

    @vbot.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        if not config.logging["is_logging"]:
            return

        self.bot.total_logs += 1
        if config.logging["url"] != "":
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    config.logging["url"], session=session)
                embed = discord.Embed(
                    title="Server Leave Logging",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="Server", value=f"`{guild.name}` ({guild.id})", inline=False)
                embed.timestamp = datetime.utcnow()
                await webhook.send(username="VBot Logging", embed=embed)

        log(f"{F.RED}Left server {F.WHITE}| {F.LIGHTBLUE_EX}{guild.name} {F.LIGHTWHITE_EX}({guild.id})")

    @vbot.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if not config.logging["is_logging"]:
            return

        self.bot.total_logs += 1
        if config.logging["url"] != "":
            channel = other.get_first_channel(guild)
            if isinstance(channel, discord.TextChannel):
                channel = channel.jump_url
            else:
                channel = channel

            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    config.logging["url"], session=session)

                embed = discord.Embed(
                    title="Server Join Logging",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Server", value=f"`{guild.name}` ({guild.id})", inline=False)
                embed.add_field(name="Server Link",
                                value=channel, inline=False)
                embed.timestamp = datetime.utcnow()
                await webhook.send(username="VBot Logging", embed=embed)

        log(f"{F.GREEN}Joined server {F.WHITE}| {F.LIGHTBLUE_EX}{guild.name} {F.LIGHTWHITE_EX}({guild.id})")

    @vbot.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if not config.logging["is_logging"]:
            return

        if member._user == self.bot.user:
            return

        self.bot.total_logs += 1
        if config.logging["url"] != "":
            channel = other.get_first_channel(member.guild)
            if isinstance(channel, discord.TextChannel):
                channel = channel.jump_url
            else:
                channel = channel

            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    config.logging["url"], session=session)
                embed = discord.Embed(
                    title="Member Leave Logging",
                    color=discord.Color.red()
                )
                embed.add_field(
                    name="User", value=f"`{member}` ({member.id})", inline=False)
                embed.add_field(
                    name="Server", value=f"`{member.guild.name}` ({member.guild.id})", inline=False)
                embed.add_field(name="Server Link",
                                value=channel, inline=False)
                embed.timestamp = datetime.utcnow()
                await webhook.send(username="VBot Logging", embed=embed)

        log(f"{F.RED}User left a server {F.WHITE}| {F.LIGHTBLUE_EX}{member} - {member.guild.name} {F.LIGHTWHITE_EX}({member.id} - {member.guild.id})")

    @vbot.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if not config.logging["is_logging"]:
            return

        if member._user == self.bot.user:
            return

        self.bot.total_logs += 1
        if config.logging["url"] != "":
            channel = other.get_first_channel(member.guild)
            if isinstance(channel, discord.TextChannel):
                channel = channel.jump_url
            else:
                channel = channel

            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    config.logging["url"], session=session)
                embed = discord.Embed(
                    title="Member Join Logging",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="User", value=f"`{member}` ({member.id})", inline=False)
                embed.add_field(
                    name="Server", value=f"`{member.guild.name}` ({member.guild.id})", inline=False)
                embed.add_field(name="Server Link",
                                value=channel, inline=False)
                embed.timestamp = datetime.utcnow()
                await webhook.send(username="VBot Logging", embed=embed)

        log(f"{F.GREEN}User joined a server {F.WHITE}| {F.LIGHTBLUE_EX}{member} - {member.guild.name} {F.LIGHTWHITE_EX}(User: {member.id} - Server: {member.guild.id})")

    @vbot.Cog.listener()
    async def on_command(self, ctx: vbot.Context):
        self.bot.total_cmds += 1

        if not config.logging["is_logging"]:
            return

        self.bot.total_logs += 1
        if config.logging["url"] != "":
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(
                    config.logging["url"], session=session)
                embed = discord.Embed(
                    title="Command Logging",
                    color=discord.Color.random()
                )
                embed.add_field(
                    name="Command", value=f"`{ctx.message.content}`", inline=False)
                if not isinstance(ctx.channel, discord.GroupChannel):
                    embed.add_field(
                        name="Server", value=f"`{ctx.guild.name}` ({ctx.guild.id})", inline=False)

                embed.add_field(
                    name="Channel", value=f"<#{ctx.channel.id}>", inline=False)
                embed.add_field(name="Message Link",
                                value=f"{ctx.message.jump_url}", inline=False)
                embed.timestamp = datetime.utcnow()
                await webhook.send(username="VBot Logging", embed=embed)

        cmd = ctx.command
        log(f"{F.GREEN}Sent command {F.WHITE}| {F.LIGHTBLUE_EX}{cmd} {F.LIGHTWHITE_EX}at {f'#{ctx.channel.name}' if not isinstance(ctx.channel, discord.DMChannel) else ctx.channel}")


if __name__ == "__main__":
    print("You need to run main.py to run the bot")


async def setup(bot):
    await bot.add_cog(Events(bot))
