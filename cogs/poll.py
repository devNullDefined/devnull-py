import discord
from discord.ext import commands


class Poll(commands.Cog):
    '''Poll using discord embed.'''
    poll_ids = []
    letters = [
        "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
        "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
    ]
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mkpoll(self, ctx, question, *options):
        poll = discord.Embed(
            title=question,
            type='rich'
        )
        poll.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
        )
        msg = await ctx.send(embed=poll)
        
        if len(options) <= 10:
            for i, option in enumerate(options):
                emoji = f'{i}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}'
                poll.add_field(
                    name=f'{emoji} - {option}',
                    value='value',
                    inline=False
                )
                await msg.edit(embed=poll)
                await msg.add_reaction(emoji)
        else:
            for i, option in enumerate(options):
                poll.add_field(
                    name=f'{self.letters[i]} - {option}',
                    value='value',
                    inline=False
                )
                await msg.edit(embed=poll)
                await msg.add_reaction(self.letters[i])


def setup(bot):
    bot.add_cog(Poll(bot))
