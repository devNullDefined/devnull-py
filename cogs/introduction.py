import discord
from discord.ext import commands


class Introduction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user.id in message.raw_mentions:
            fetch = discord.Embed(
                title=self.bot.user.name,
                type='rich',
                description=f'**Prefix:** `{self.bot.command_prefix}`',
                color=0x336d9d,
                url='https://github.com/devNullDefined/devnull-py'
            )
            fetch.set_author(
                name=message.guild.name,
                url='https://github.com/devNullDefined',
                icon_url=message.guild.icon_url
            )
            fetch.set_thumbnail(
                url=self.bot.user.avatar_url
            )
            await message.channel.send(embed=fetch)


def setup(bot):
    bot.add_cog(Introduction(bot))
