import traceback
import sys
from selfcord.ext import commands as vbot


class ErrorHandler(vbot.Cog):
    def __init__(self, bot):
        self.bot: vbot.Bot = bot

    @vbot.Cog.listener()
    async def on_command_error(self, ctx: vbot.Context, error):
        cog = ctx.cog
        msg = ctx.message

        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error = getattr(error, 'original', error)

        if isinstance(error, vbot.CommandNotFound):
            await msg.edit(content=f"```yaml\n❌ The command \"{msg.content.split(' ')[0]}\" does not exist.```", delete_after=5)

        elif isinstance(error, vbot.MissingRequiredArgument):
            await msg.edit(content=f"```yaml\n❌ You forgot to write the parameter \"{error.param.name}\".```", delete_after=5)

        elif isinstance(error, vbot.BadArgument):
            await msg.edit(content=f"```yaml\n❌ You entered a parameter incorrectly.```", delete_after=5)

        elif isinstance(error, vbot.MissingPermissions):
            await msg.edit(content=f"```yaml\n❌ You don't have enough permissions to perform this command.```", delete_after=5)

        elif isinstance(error, Exception):
            await msg.edit(content=f"```yaml\n❌ An unknown error occurred: {error}```", delete_after=5)

        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
