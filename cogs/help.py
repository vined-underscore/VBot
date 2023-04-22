import main
import selfcord as discord
from selfcord.ext import commands as vbot

invisible_cogs = ['nitro sniper', 'events', 'errorhandler']


class HelpCommand(vbot.HelpCommand):
    async def send_bot_help(self, mapping) -> None:
        desc = []
        for cog, cmds in mapping.items():
            if cog is None or cog.qualified_name.lower() in invisible_cogs:
                continue

            cmds = await self.filter_commands(cmds, sort=True)
            desc.append(f"- {cog.qualified_name}: {len(cmds)} commands")

        desc = "\n".join(desc)

        msg = f"""```yaml
> Made by {self.context.bot.get_user(main.__author_id__)} | {main.__author_id__} <

# {len([command for command in self.context.bot.walk_commands()])} Commands (and subcommands) # VBot v{main.__version__}

< ---|-
    
{desc}

-|--- >

!# Run {self.context.clean_prefix}{self.invoked_with} [category] to learn more about a category and its commands
!# The category name must be case-sensitive. Example: "{self.context.clean_prefix}help Raiding"```"""
        await self.context.message.edit(content=msg, delete_after=15)

    async def send_group_help(self, group: vbot.Group) -> None:
        desc = ""
        cmd_desc = \
            f"Name: {group.name}\nCategory: {group.cog_name}\nInfo: {group.description.replace('PREFIX', self.context.clean_prefix)}\n\n" \
            f"Aliases:\n - {', '.join(group.aliases) if group.aliases else 'None'}\n\n" \
            f"Usage: {self.context.clean_prefix}{group.name} {group.signature}" if not group.full_parent_name else f"Usage: {self.context.clean_prefix}{group.full_parent_name} {group.name} {group.signature}"

        cmds = await self.filter_commands(group.commands, sort=True)
        for idx, c in enumerate(cmds):
            desc += f"  - {self.context.clean_prefix}{c.qualified_name}: {c.description.replace('PREFIX', self.context.clean_prefix) or 'No help information'}"
            
            if len(c.description) > 50 and idx != len(cmds) - 1:
                desc += f"\n\n"
            elif idx != len(cmds) - 1:
                desc += f"\n"
            
        msg = f"""```yaml
> Made by {self.context.bot.get_user(main.__author_id__)} | {main.__author_id__} <

Group Info: {group.qualified_name}

< ---|-
    
{cmd_desc}

Group Commands:
{desc}

-|--- >

!# [optional], <required>, "=" indicates the default value
!# Run {self.context.clean_prefix}{self.invoked_with} {group.name} [subcommand] to learn more about a subcommand```"""
        await self.context.message.edit(content=msg, delete_after=15)

    async def send_command_help(self, cmd: vbot.Command) -> None:
        desc = f"""Name: {cmd.name}\nCategory: {cmd.cog_name}\nInfo: {cmd.description.replace('PREFIX', self.context.clean_prefix)}\n
Aliases:\n - {', '.join(cmd.aliases) if cmd.aliases else 'None'}\n
Usage: {f"{self.context.clean_prefix}{cmd.name} {cmd.signature}" if not cmd.full_parent_name else f"{self.context.clean_prefix}{cmd.full_parent_name} {cmd.name} {cmd.signature}"}"""
        msg = f"""```yaml
> Made by {self.context.bot.get_user(main.__author_id__)} | {main.__author_id__} <

Command Info: {cmd.qualified_name}

< ---|-
    
{desc}

-|--- >

!# [optional], <required>, "=" indicates the default value```"""
        await self.context.message.edit(content=msg, delete_after=15)

    async def send_cog_help(self, cog: vbot.Cog) -> None:
        cmds = await self.filter_commands(cog.get_commands(), sort=True)
        cmds = "\n".join(
            f"- {self.context.clean_prefix}{cmd.name}: {cmd.description.replace('PREFIX', self.context.clean_prefix)}" for cmd in cmds)
        msg = f"""```yaml
> Made by {self.context.bot.get_user(main.__author_id__)} | {main.__author_id__} <

Category Info: {cog.qualified_name}

< ---|-
    
{cmds}

-|--- >

!# Run {self.context.clean_prefix}{self.invoked_with} [command] to learn more about a command```"""
        await self.context.message.edit(content=msg, delete_after=15)

    def command_not_found(self, string: str, /) -> str:
        return f"```yaml\n- No command called \"{string}\" found.\n- Use \"{self.context.clean_prefix}help\" to see a list of all the commands.```"

    def subcommand_not_found(self, command, sub: str, /) -> str:
        if isinstance(command, vbot.Group) and len(command.all_commands) > 0:
            return f"```yaml\n- Command \"{command.qualified_name}\" has no subcommand named \"{sub}\".\n- Do \"{self.context.clean_prefix}help [{command.qualified_name}]\" to see a list of all the subcommands.```"

        return f"```yaml\n- Command \"{command.qualified_name}\" has no subcommands.```"

    async def send_error_message(self, error: str) -> None:
        await self.context.message.edit(error, delete_after=5)


async def setup(client):
    client._default_help_command = client.help_command
    client.help_command = HelpCommand()


def teardown(client):
    client.help_command = client._default_help_command
