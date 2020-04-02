import discord
from discord.ext import commands
import json
import asyncio
from random import randint, choice, randrange

with open('config.json', 'r') as cfg:
    config = json.load(cfg)
    
bot = commands.Bot(command_prefix=config['prefix'])


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
    await ctx.send(choice(['Heads', 'Tails']))


@bot.command()
async def roll(ctx, *args):
    if len(args) == 0:
        n = randint(0, 100)
    elif len(args) == 1:
        n = randint(0, int(args[0]))
    elif len(args) == 2:
        n = randint(int(args[0]), int(args[1]))

    await ctx.send(n)


@bot.command()
async def countdown(ctx, seconds: int):
    msg = await ctx.send(f'**{seconds}**')

    for i in range(seconds-1, -1, -1):
        await asyncio.sleep(1)
        await msg.edit(content=f'**{i}**')


@bot.command()
async def emojiname(ctx, emoji):
    '''Print encoded emojiname.'''
    await ctx.send(emoji.encode('ascii', 'namereplace'))


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


bot.run(config['token'])
