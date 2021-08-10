from discord.ext import commands
from random import randint, choice
import discord
import asyncio


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *args):
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(' '.join(args))

    @commands.command()
    async def flip(self, ctx):
        flipped = choice(['Heads', 'Tails'])
        await ctx.send(f'**{flipped}**')

    @commands.command()
    async def roll(self, ctx, *args: int):
        if len(args) == 0: args = [0, 100]
        elif len(args) == 1: args = [args[0], 0]
        elif len(args) == 2: args = list(args)
        args.sort()
        await ctx.send(randint(*args))

    @commands.command()
    async def countdown(self, ctx, seconds: int, msg=None):
        '''Counts down from <seconds> and optionally sends <msg> after'''
        try:
            await ctx.message.delete()
        except:
            pass

        if seconds < 3:
            await ctx.send('Min seconds = 3')
            return
        if seconds > 120:
            await ctx.send('Max seconds = 120')
            return

        sent = await ctx.send(f'**{seconds}**')
        for i in range(seconds-1, -1, -1):
            await asyncio.sleep(1)
            if i == 0 and msg:
                await sent.edit(content=f'**{msg}**')
            else:
                await sent.edit(content=f'**{i}**')


def setup(bot):
    bot.add_cog(Fun(bot))
