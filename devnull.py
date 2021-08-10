from discord.ext import commands
import discord
import asyncio
import json
import os


def get_prefix(bot, msg):
    return os.environ['PREFIX']


intents = discord.Intents.all()
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_ready():
    print('Ready!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(bot.get_emoji(694341216267010078))
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Missing required argument {bot.get_emoji(667775700538753034)}')
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'Absolute bullshit argument {bot.get_emoji(629773774920744990)}')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(f'If you think you can do that... {bot.get_emoji(668526049277247498)}')
    elif isinstance(error, commands.NotOwner):
        await ctx.send(f'You are not that guy pal {bot.get_emoji(694344505431949323)}')
    raise error


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.environ['TOKEN'])
