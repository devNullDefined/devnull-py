import discord
from discord.ext import commands


class Poll(commands.Cog):
    '''Poll using discord embed.'''
    polls = {}
    letters = [
        "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
        '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER D}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER E}', 
        '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER G}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER J}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER M}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER P}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER S}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER V}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER Y}',
        '\N{REGIONAL INDICATOR SYMBOL LETTER Z}'
    ]
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mkpoll(self, ctx, question, *options):
        description = ''

        for i in range(len(options)):
            description += f'\n{self.letters[i]} **{options[i]}**'

        poll = discord.Embed(title=question, type='rich', description=description)
        poll.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=poll)
        self.polls[msg.id] = ctx.author.id
        await ctx.message.delete()
        
        for i in range(len(options)):
            await msg.add_reaction(self.letters[i])

    async def custom_check(self, ctx, msg_id):
        '''Checks if poll is active and it's author is the one trying to edit it.'''
        if msg_id in self.polls:
            if ctx.author.id == self.polls[msg_id]:
                return True
            else:
                await ctx.send('You are not the author of this poll.')
        else:
            await ctx.send('No active poll found with given id.')
        return False

    @commands.command()
    async def chpoll_question(self, ctx, msg_id: int, new_question):
        check_passed = await self.custom_check(ctx, msg_id)
        if not check_passed:
            return
        msg = await ctx.fetch_message(msg_id)
        poll_dict = msg.embeds[0].to_dict()
        poll_dict['title'] = new_question
        await msg.edit(embed=discord.Embed.from_dict(poll_dict))

    @commands.command()
    async def chpoll_options(self, ctx, msg_id: int, *new_options):
        check_passed = await self.custom_check(ctx, msg_id)
        if not check_passed:
            return
        msg = await ctx.fetch_message(msg_id)
        poll_dict = msg.embeds[0].to_dict()
        poll_dict['description'] = ''
        
        for i in range(len(new_options)):
            poll_dict['description'] += f'\n{self.letters[i]} **{new_options[i]}**'
            await msg.add_reaction(self.letters[i])

        if len(new_options) < len(msg.reactions):
            for reaction in msg.reactions[len(new_options):]:
                await msg.clear_reaction(reaction.emoji)

        await msg.edit(embed=discord.Embed.from_dict(poll_dict))
            

    @commands.command()
    async def chpoll_option(self, ctx, msg_id: int, emoji, new_option):
        check_passed = await self.custom_check(ctx, msg_id)
        if not check_passed:
            return
        msg = await ctx.fetch_message(msg_id)
        poll_dict = msg.embeds[0].to_dict()
        options = poll_dict['description'].split('\n')
        for option in options:
            if option.startswith(emoji):
                poll_dict['description'] = poll_dict['description'].replace(option, f'{emoji} **{new_option}**')
                await msg.edit(embed=discord.Embed.from_dict(poll_dict))
                return

    @commands.command()
    async def addpoll_option(self, ctx, msg_id: int, new_option):
        if msg_id not in self.polls:
            await ctx.send('No active poll found with given id.')
            return
        msg = await ctx.fetch_message(msg_id)
        poll_dict = msg.embeds[0].to_dict()
        new_option_id = len(poll_dict['description'].split('\n'))
        poll_dict['description'] += f'\n{self.letters[new_option_id]} **{new_option}**'
        await msg.edit(embed=discord.Embed.from_dict(poll_dict))
        await msg.add_reaction(self.letters[new_option_id])

    @commands.command()
    async def close_poll(self, ctx, msg_id: int):
        check_passed = await self.custom_check(ctx, msg_id)
        if not check_passed:
            return
        msg = await ctx.fetch_message(msg_id)
        poll_dict = msg.embeds[0].to_dict()
        counts = [reaction.count for reaction in msg.reactions]
        overall_reactions = sum(counts) - len(counts)
        top_reaction = msg.reactions[counts.index(max(counts))]

        for option in msg.embeds[0].to_dict()['description'].split('\n'):
            if option.startswith(top_reaction.emoji):
                description = f'{(top_reaction.count - 1) // overall_reactions * 100}% votes for **{option[2:]}**'
                closure = discord.Embed(title=poll_dict['title'], type='rich', description=description, colour=discord.Colour.green())

        sent_msg = await ctx.send(f'Poll closed: {msg.jump_url}')
        self.polls.pop(msg_id)
        await sent_msg.edit(embed=closure)

    @commands.command()
    async def active_polls(self, ctx):
        if len(self.polls) == 0:
            await ctx.send('There are no active polls.')
        else:
            jump_urls = [(await ctx.fetch_message(msg_id)).jump_url for msg_id in self.polls]
            await ctx.send('\n'.join(jump_urls))


def setup(bot):
    bot.add_cog(Poll(bot))
