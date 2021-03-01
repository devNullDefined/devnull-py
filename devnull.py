from random import randint, choice, randrange
from discord.ext import commands
import discord
import asyncio
import json
import os

bot = commands.Bot(command_prefix=os.environ['PREFIX'])
music_playlist = []

@bot.event
async def on_ready():
    print('Ready!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('პრეფიქსები ხომ არ აგერია')
    raise error

@bot.command()
async def say(ctx, *args):
    await ctx.send(' '.join(args))

@bot.command()
async def flip(ctx):
    flipped = choice(['Heads', 'Tails'])
    await ctx.send(f'**{flipped}**')

@bot.command()
async def roll(ctx, *args: int):
    if len(args) == 0: args = [0, 100]
    elif len(args) == 1: args = [args[0], 0]
    elif len(args) == 2: args = list(args)
    args.sort()
    await ctx.send(randint(*args))

@bot.command()
async def countdown(ctx, seconds: int):
    '''Countdown from <seconds> (min value = 3; max = 120)'''
    if seconds in range(3, 121):
        msg = await ctx.send(f'**{seconds}**')

        for i in range(seconds-1, -1, -1):
            await asyncio.sleep(1)
            await msg.edit(content=f'**{i}**')
    else:
        await ctx.send('min seconds = 3; max = 120')

@bot.command()
async def emojiname(ctx, emoji):
    '''Print encoded emojiname.'''
    await ctx.send(emoji.encode('ascii', 'namereplace'))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.environ['TOKEN'])
