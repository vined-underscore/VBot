import traceback
import sys
from utils.other import log_error
from discord.ext import commands as vbot


class ErrorHandler(vbot.Cog):
    def __init__(self, bot: vbot.Bot):
        self.bot = bot

    @vbot.Cog.listener()
    async def on_command_error(self, ctx: vbot.Context, error):
        cog = ctx.cog
        msg = ctx.message

        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error = getattr(error, 'original', error)

        if isinstance(error, vbot.CommandNotFound):
            await log_error(ctx, error, f"```yaml\n❌ The command \"{msg.content.split(' ')[0]}\" does not exist.```")

        elif isinstance(error, vbot.MissingRequiredArgument):
            await log_error(ctx, error, f"```yaml\n❌ You forgot to write the parameter \"{error.param.name}\".```")

        elif isinstance(error, vbot.BadArgument):
            await log_error(ctx, error, f"```yaml\n❌ You entered a parameter incorrectly.```")

        elif isinstance(error, vbot.MissingPermissions):
            await log_error(ctx, error, f"```yaml\n❌ You don't have enough permissions to perform this command.```")

        else:
            await log_error(ctx, error, f"```yaml\n❌ An unknown error occurred: {error}```", True)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)


async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
