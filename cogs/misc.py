import discord
import psutil
import config
from colorama import Fore as F
from discord.ext import commands as vbot
from utils import alias
from humanfriendly import format_size


class MiscCmds(
        vbot.Cog,
        name="Misc",
        description="Various miscellanous commands"):
    def __init__(self, bot: vbot.Bot):
        self.bot = bot

    @vbot.command(
        name="listening",
        description="Sets your status to Listening"
    )
    async def listening(self, ctx: vbot.Context, *, activity_message: str = "VBot"):
        msg = ctx.message

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=activity_message,),
            status=self.bot.status)

        await msg.edit(content=f"```yaml\n+ Set your listening status to {activity_message}```", delete_after=5)

    @vbot.command(
        name="watching",
        description="Sets your status to Watching"
    )
    async def watching(self, ctx: vbot.Context, *, activity_message: str = "VBot"):
        msg = ctx.message

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=activity_message),
            status=self.bot.status)

        await msg.edit(content=f"```yaml\n+ Set your watching status to {activity_message}```", delete_after=5)

    @vbot.command(
        name="playing",
        description="Sets your status to Playing"
    )
    async def playing(self, ctx: vbot.Context, *, activity_message: str = "VBot"):
        msg = ctx.message

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name=activity_message),
            status=self.bot.status)

        await msg.edit(content=f"```yaml\n+ Set your playing status to {activity_message}```", delete_after=5)

    @vbot.command(
        name="stopactivity",
        description="Stops your current activity",
        aliases=alias.get_aliases("stopactivity")
    )
    async def stopactivity(self, ctx: vbot.Context):
        await ctx.message.delete()
        await self.bot.change_presence(
            activity=None,
            status=self.bot.status)

    @vbot.group(
        name="status",
        description="Changes your status",
        invoke_without_command=True
    )
    async def status(self, ctx: vbot.Context):
        msg = ctx.message
        await msg.edit(content=f"```yaml\n- Incorrect usage. Correct usage: {ctx.clean_prefix}help [status]```", delete_after=5)

    @status.command(
        name="dnd",
        description="Changes your status to do not disturb"
    )
    async def dnd(self, ctx: vbot.Context):
        msg = ctx.message
        await self.bot.change_presence(status=discord.Status.dnd)
        await msg.edit(content=f"```yaml\nChanged status to do not disturb.```", delete_after=5)

    @status.command(
        name="idle",
        description="Changes your status to idle"
    )
    async def idle(self, ctx: vbot.Context):
        msg = ctx.message
        await self.bot.change_presence(status=discord.Status.idle)
        await msg.edit(content=f"```yaml\nChanged status to idle.```", delete_after=5)

    @status.command(
        name="offline",
        description="Changes your status to offline"
    )
    async def offline(self, ctx: vbot.Context):
        msg = ctx.message
        await self.bot.change_presence(status=discord.Status.invisible)
        await msg.edit(content=f"```yaml\nChanged status to offline```", delete_after=5)

    @status.command(
        name="online",
        description="Changes your status to online"
    )
    async def online(self, ctx: vbot.Context):
        msg = ctx.message
        await self.bot.change_presence(status=discord.Status.online)
        await msg.edit(content=f"```yaml\nChanged status to online.```", delete_after=5)

    @status.command(
        name="none",
        description="Changes your status to none (Gives priority over your discord app status)"
    )
    async def none(self, ctx: vbot.Context):
        msg = ctx.message
        await self.bot.change_presence(status=None)
        await msg.edit(content=f"```yaml\nChanged status to none.```", delete_after=5)

    @vbot.command(
        name="clearconsole",
        description="Clears the console"
    )
    async def clearconsole(self, ctx: vbot.Context):
        await ctx.message.delete()
        await self.bot.full_banner()

    @vbot.command(
        name="ping",
        description="Sends the bot latency",
        aliases=alias.get_aliases("ping")
    )
    async def ping(self, ctx: vbot.Context):
        msg = ctx.message
        latency = round(self.bot.latency * 1000)
        await msg.edit(content=f"```yaml\nThe bot's latency is {latency}ms```", delete_after=5)

    @vbot.command(
        name="botstats",
        description="Sends information about the PC and bot"
    )
    async def botstats(self, ctx: vbot.Context):
        msg = ctx.message
        guilds = len(self.bot.guilds)
        users = len(self.bot.users)
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        nl = "\n"
        # ugly ass code
        await msg.edit(content=f"""```yaml
- Bot Stats:
    * Bot Uptime: {self.bot.get_uptime()}
    * Servers: {guilds}
    * Users: {users}
    * Messages Received: {self.bot.total_msgs}
    * Commands Used: {self.bot.total_cmds}{f'{nl}    * Nitro Sniped: {self.bot.nitro_sniped}' if config.snipers["nitro_sniper"]["enabled"] else ""}{f'{nl}    * Invites Found: {self.bot.invites_found}' if config.snipers["invite_sniper"]["enabled"] else ""}{f'{nl}    * Keywords Found: {self.bot.keywords_found}' if config.snipers["keyword_sniper"]["enabled"] else ""}
    
- Logging Stats:
    * Logging: {config.logging["is_logging"]}
    * Error Logging: {config.logging["error_logging"] if config.logging["error_logging"] != "" else "disabled"}
    * Logs Amount: {self.bot.total_logs}

- PC Stats:
    * CPU Usage: {cpu}% (not accurate)
    * RAM Usage: {ram.percent}%
    * Total RAM: {format_size(ram.total)}
    * Available RAM: {format_size(ram.available)}
    * Total Disk Space: {format_size(disk.total)}
    * Used Disk Space: {format_size(disk.used)}
    * Free Disk Space: {format_size(disk.free)}
    * Disk Usage: {disk.percent}%```""", delete_after=15)


if __name__ == "__main__":
    print("You need to run main.py to run the bot")


async def setup(bot):
    await bot.add_cog(MiscCmds(bot))
