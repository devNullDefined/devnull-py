from discord.ext import commands
from discord.ext.commands import CommandNotFound
import discord
import asyncio
import json
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.environ['PREFIX'], intents=intents)

@bot.event
async def on_ready():
    print('Ready!')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f'მაგაზე პასუხი არ მაქვს, მგონი პრეფიქსი აგერია {bot.get_emoji(645706036292091904)}')
    raise error


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.environ['TOKEN'])
