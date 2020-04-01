import discord
from discord.ext import commands
import json

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

    
@bot.listen()
async def on_message(message):
    if bot.user.id in message.raw_mentions:
        fetch = discord.Embed(
            title=bot.user.name,
            type='rich',
            description=f'**Prefix:** `{bot.command_prefix}`',
            color=0x336d9d,
            url='https://github.com/defnullined/devnull-py'
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
