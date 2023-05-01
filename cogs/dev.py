import os
import main
import sys
import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
from utils import alias
from discord.ext import commands as vbot
from colorama import Fore


class DevCmds(
        vbot.Cog,
        name="Dev",
        description="Various commands to manage the bot"):
    def __init__(self, bot: vbot.Bot):
        self.bot = bot
        self.folder = main.__cog_folder__

    @vbot.command(
        name="restart",
        description="Restarts the bot"
    )
    async def restart(self, ctx: vbot.Context):
        await ctx.message.delete()
        os.execv(sys.executable, ['python'] + ['./main.py'])

    @vbot.command(
        name="logout",
        description="Logs you out of the bot",
        aliases=alias.get_aliases("logout")
    )
    async def logout(self, ctx: vbot.Context):
        await ctx.message.delete()
        print(
            f"{Fore.GREEN}[+]{Fore.LIGHTWHITE_EX} Logged out of the account {Fore.LIGHTBLUE_EX}{self.bot.user}")
        await self.bot.close()

    @vbot.command(
        name="load",
        description="Load a cog or load all by using \"*\" or \"all\""
    )
    async def load(self, ctx: vbot.Context, cog: str):
        msg = ctx.message
        if cog == "*" or cog == "all":
            await msg.edit(content="```yaml\nLoading all cogs...````")

            for filename in os.listdir(self.folder):
                if filename.endswith('.py'):
                    try:
                        await self.bot.load_extension(f'{self.folder}.{filename[:-3]}')
                        await msg.edit(content=f"```yaml\nSuccesfully loaded cog \"{filename}\"```", delete_after=5)

                    except Exception as e:
                        await msg.edit(content=f"```yaml\n{e}```", delete_after=5)
                        return

            return await msg.edit(content="```yaml\nLoaded all cogs```", delete_after=5)

        print(f"Trying to load cog {cog}...")
        await msg.edit(content=f"```yaml\nLoading cog \"{cog}.py\"...```")

        try:
            await self.bot.load_extension(f"{self.folder}.{cog}")
            print(f"Succesfully loaded cog {cog}")
            await msg.edit(content=f"```yaml\nSuccesfully loaded cog \"{cog}.py\"```")

        except Exception as e:
            await msg.edit(content=f"```yaml\n{e}```", delete_after=5)

    @vbot.command(
        name="unload",
        description="Unload a cog or unload all by using \"*\" or \"all\""
    )
    async def unload(self, ctx: vbot.Context, cog: str):
        msg = ctx.message

        if cog == "*" or cog == "all":
            await msg.edit(content="```yaml\nUnloading all cogs...```")
            for filename in os.listdir(self.folder):
                if filename.startswith("dev"):
                    continue

                if filename.endswith('.py'):
                    try:
                        await self.bot.unload_extension(f'{self.folder}.{filename[:-3]}')
                        await msg.edit(content=f"```yaml\nSuccesfully unloaded cog \"{filename}\"```")

                    except Exception as e:
                        await msg.edit(content=f"```yaml\n{e}```", delete_after=5)
                        return

            return await msg.edit(content="```yaml\nUnloaded all cogs!```", delete_after=5)

        await msg.edit(content=f"```yaml\nUnloading cog \"{cog}.py\"...```")

        try:
            await self.bot.unload_extension(f"{self.folder}.{cog}")
            await msg.edit(content=f"```yaml\nSuccesfully unloaded cog \"{cog}.py\"```")

        except Exception as e:
            await msg.edit(content=f"```yaml\n{e}```", delete_after=5)

    @vbot.command(
        name="reload",
        description="Reload a cog or reload all by using \"*\" or \"all\""
    )
    async def reload(self, ctx: vbot.Context, cog: str):
        msg = ctx.message

        if cog == "*" or cog == "all":
            await msg.edit(content="```yaml\nReloading all cogs...```")
            for filename in os.listdir(self.folder):
                if filename.endswith('.py'):
                    try:
                        await self.bot.reload_extension(f'{self.folder}.{filename[:-3]}')
                        await msg.edit(content=f"```yaml\nSuccesfully reloaded cog \"{filename}\"```")

                    except Exception as e:
                        await msg.edit(content=f"```yaml\n{e}```", delete_after=5)
                        return

            return await msg.edit(content="```yaml\nReloaded all cogs```", delete_after=5)

        await msg.edit(content=f"```yaml\nReloading cog \"{cog}.py\"```")

        try:
            await self.bot.reload_extension(f'{self.folder}.{cog}')
            await msg.edit(content=f"```yaml\nSuccesfully reloaded cog \"{cog}.py\"```", delete_after=5)

        except Exception as e:
            await msg.edit(content=f"```yaml\n{e}```", delete_after=5)

    @vbot.command(
        name='eval',
        description="Run python code in discord",
        aliases=alias.get_aliases("eval")
    )
    # not mine lol
    async def _eval(self, ctx: vbot.Context, *, code: str):
        def cleanup_code(self, content):
            # remove ```py\n```
            if content.startswith('```') and content.endswith('```'):
                return '\n'.join(content.split('\n')[1:-1])

            # remove `foo`
            return content.strip('` \n')

        env = {
            'bot': self.bot,
            'self': self,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            'source': inspect.getsource,
        }

        env.update(globals())

        body = cleanup_code(self, code)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            '''Simple generator that paginates text.'''
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text) - 1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != '', pages))

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            return await ctx.message.add_reaction('\u2049')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:

                        out = await ctx.send(f'```py\n{value}\n```')
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')
            else:
                self.bot._last_result = ret
                try:
                    out = await ctx.send(f'```py\n{value}{ret}\n```')
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')

        if out:
            await ctx.message.add_reaction('\u2705')  # tick
        elif err:
            await ctx.message.add_reaction('\u2049')  # x
        else:
            await ctx.message.add_reaction('\u2705')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


if __name__ == "__main__":
    print("You need to run main.py to run the bot")


async def setup(bot):
    await bot.add_cog(DevCmds(bot))
