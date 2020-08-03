import discord
from discord.ext import commands
import os
import json
import asyncio
from random import randint, choice, randrange

bot = commands.Bot(command_prefix=os.environ['PREFIX'])

@bot.event
async def on_ready():
    print('Ready!')
    watching = discord.Activity(type=discord.ActivityType.watching, name='Luke Smith')
    await bot.change_presence(activity=watching)


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


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')


@bot.listen()
async def on_message(message):
    if bot.user.id in message.raw_mentions:
        fetch = discord.Embed(
            title=bot.user.name,
            type='rich',
            description=f'**Prefix:** `{bot.command_prefix}`',
            color=0x336d9d,
            url='https://github.com/devNullDefined/devnull-py'
        )
        fetch.set_author(
            name=message.guild.name,
            url='https://github.com/devNullDefined',
            icon_url=message.guild.icon_url
        )
        fetch.set_thumbnail(
            url=bot.user.avatar_url
        )
        await message.channel.send(embed=fetch)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(os.environ['TOKEN'])

