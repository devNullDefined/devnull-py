import os
import json
import asyncio
import discord
from discord.ext import commands
from random import randint, choice, randrange

bot = commands.Bot(command_prefix=os.environ['PREFIX'])
music_playlist = []

@bot.event
async def on_ready():
    print('Ready!')


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


@bot.listen()
async def on_message(message):
    # temporarily for Halloween shit
    if message.author.id == 755580145078632508 and message.channel.id == 767342376997224468:
        if message.embeds[0].to_dict()['title'] == 'A trick-or-treater has stopped by!':
            await message.channel.send(message.guild.get_member(244461918243389442).mention)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.environ['TOKEN'])

