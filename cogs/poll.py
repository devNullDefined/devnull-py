import discord
from discord.ext import commands


class Poll(commands.Cog):
    '''Poll using discord embed.'''
    polls = {}
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
        data = {'author_id': ctx.author.id, 'author_name': ctx.author.name, 'question': question, 'inner': {}}
        
        for i, option in enumerate(options):
            if len(options) <= 10:
                emoji = f'{i}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}'
            else:
                emoji = self.letters[i]
            data['inner'][emoji] = {'option': option, 'votes': 0, 'voters': []}

        description = '\n'.join([f'{emoji} `0` **{info["option"]}**' for emoji, info in data['inner'].items()])
        poll = discord.Embed(title=question, type='rich', description=description)
        poll.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=poll)
        self.polls[str(msg.id)] = data
        poll.set_footer(text=f'Poll id: {msg.id}', icon_url=self.bot.user.avatar_url)
        await msg.edit(embed=poll)
        
        for emoji in data['inner'].keys():
            await msg.add_reaction(emoji)

    @classmethod
    async def update_poll(cls, msg):
        max_vote_len = len(str(max([i['votes'] for i in cls.polls[str(msg.id)]['inner'].values()])))
        description = []

        for emoji, info in cls.polls[str(msg.id)]['inner'].items():
            dif = max_vote_len - len(str(info['votes']))
            description.append(f'{emoji} `{dif*"0"}{info["votes"]}` **{info["option"]}**')
                
        poll = msg.embeds[0]
        poll.description = '\n'.join(description)
        await msg.edit(embed=poll)

    @classmethod
    def find_poll(cls, emoji):
        found_poll_ids = []
        for _id, info in cls.polls.items():
            if emoji in info['inner'].keys():
                found_poll_ids.append(_id)
        return found_poll_ids

    @classmethod
    async def check_if_already_voted(cls, strict_check, poll, author_id):
        for i in cls.polls[str(poll.id)]['inner'].values():
            for voter in i['voters']:
                if author_id == voter:
                    return True

        reacted = 0
        for reaction in poll.reactions:
            users = await reaction.users().flatten()
            for user in users:
                if author_id == user.id:
                    if strict_check:
                        return True
                    reacted += 1
                    if reacted > 1:
                        return True
        return False
        
    @commands.command()
    async def vote(self, ctx, emoji, poll_id: int=None):
        if self.polls:
            if not poll_id:
                target_poll_ids = self.find_poll(emoji)
                if target_poll_ids:
                    if len(target_poll_ids) == 1:
                        poll_id = int(target_poll_ids[0])
                    else:
                        text = f'```xl\n{len(self.polls)} polls are active at this moment:'
                        for i, _id in enumerate(target_poll_ids):
                            text += f'\n{i} {_id} ({self.polls[_id]["question"]})'
                        text += '\nwrite index or whole id```'
                        tmp = await ctx.send(text)
                        
                        def check(m):
                            return m.author == ctx.author
                        
                        answer = await self.bot.wait_for('message', timeout=60.0, check=check)
                        await tmp.delete()
                        await answer.delete()
                        try:
                            i = int(answer.content)
                        except:
                            await ctx.message.add_reaction('\N{CROSS MARK}')
                        else:
                            if answer.content not in target_poll_ids:
                                if i < len(target_poll_ids):
                                    poll_id = int(target_poll_ids[i])
                                else:
                                    tmp = await ctx.send('Youdedwrong')
                            else:
                                poll_id = i
                else:
                    await ctx.message.add_reaction('\N{CROSS MARK}')
                    tmp = await ctx.send('That emoji is not used in any active polls')

                await ctx.message.delete(delay=5.0)
                await tmp.delete(delay=5.0)
                                    
            poll = await ctx.channel.fetch_message(poll_id)
            already_voted = await self.check_if_already_voted(True, poll, ctx.author.id)
            if already_voted:
                await ctx.message.add_reaction('\N{CROSS MARK}')
                tmp = await ctx.send(f'{ctx.author.mention} You have already voted!')
            else:
                await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                self.polls[str(poll_id)]['inner'][emoji]['votes'] += 1
                self.polls[str(poll_id)]['inner'][emoji]['voters'].append(ctx.author.id)
                await self.update_poll(poll)
        else:
            await ctx.message.add_reaction('\N{CROSS MARK}')
            tmp = await ctx.send('No active poll to vote')
        await ctx.message.delete(delay=5.0)
        try:
            await tmp.delete(delay=5.0)
        except:
            pass
        
    @commands.Cog.listener('on_reaction_add')
    @commands.Cog.listener('on_reaction_remove')
    async def update_poll_votes(self, reaction, user):
        _id, emoji = str(reaction.message.id), str(reaction.emoji)

        if _id in self.polls.keys() and user != self.bot.user:
            already_voted = await self.check_if_already_voted(False, reaction.message, user.id)
            if already_voted:
                tmp = await reaction.message.channel.send(f'{user.mention} you have already voted!')
                await tmp.delete(delay=5.0)
            else:
                self.polls[_id]['inner'][emoji]['votes'] = reaction.count - 1
                await self.update_poll(reaction.message)


def setup(bot):
    bot.add_cog(Poll(bot))
