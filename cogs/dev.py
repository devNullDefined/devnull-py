from discord.ext import commands
import discord
import os


class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        await ctx.send('https://github.com/devNullDefined/devnull-py')

    @commands.command()
    async def about_emoji(self, ctx, *emojis):
        '''Sends some useful info of emoji(s)'''
        converter = commands.EmojiConverter()
        for emoji in emojis:
            info = f'Encoded :: {emoji.encode("ascii", "namereplace")}'
            try:
                e = await converter.convert(ctx, emoji)
            except:
                continue
            else:
                info += f'\nEmojiID :: {e.id}\nURL     :: {e.url}'
            finally:
                await ctx.send(f'```asciidoc\n{info}```')


def setup(bot):
    bot.add_cog(Dev(bot))
