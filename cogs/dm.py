import selfcord as discord
import asyncio
import random
from selfcord.ext import commands as vbot


class DMCmds(
        vbot.Cog,
        name="DM",
        description="Various DM spam commands"):
    def __init__(self, bot):
        self.bot: vbot.Bot = bot

    @vbot.command(
        name="pin",
        description="Spam pins a message. If you don't put a message it will randomly select one from the DMs. (Doesn't work with system messages such as \"{user} pinned a message...\")"
    )
    async def pin(self, ctx: vbot.Context, user: discord.User, amount=15, *, msg=None):
        cmsg = ctx.message

        if amount > 100:
            return await cmsg.edit(content="```yaml\n- Max amount is 100```", delete_after=5)

        try:
            user = await self.bot.fetch_user(user.id)

        except:
            return await cmsg.edit(content="```yaml\n- Error: Invalid User```", delete_after=5)

        if not msg:
            msgs = []

            async for message in user.history(limit=10):
                msgs.append(message)

            if msgs == []:
                try:
                    message = await user.send("Hello")

                except:
                    pass

            else:
                try:
                    message = random.choice(msgs)

                except:
                    pass

        else:
            try:
                message = await user.send(msg)

            except:
                pass

        for _ in range(amount):
            await message.pin()
            await asyncio.sleep(0.5)
            await message.unpin()

        await cmsg.delete(delay=5)

    @vbot.command(
        name="unpin",
        description="Unpin an amount of messages in a persons DMs"
    )
    async def unpin(self, ctx: vbot.Context, user: discord.User, amount=15):
        count = 0
        msg = ctx.message

        if amount > 50:
            await msg.edit(content="```yaml\n- Max amount is 50```", delete_after=5)

        try:
            user = await self.bot.fetch_user(user.id)

        except:
            return await msg.edit(content="```yaml\n- Error: Invalid User```", delete_after=5)

        for pin_msg in await user.pins():
            count += 1
            if count > amount:
                return await msg.delete(delay=5)

            await pin_msg.unpin()


if __name__ == "__main__":
    print("You need to run main.py to run the bot")


async def setup(bot):
    await bot.add_cog(DMCmds(bot))
