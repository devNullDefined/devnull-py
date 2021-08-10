from discord.ext import tasks, commands
from bs4 import BeautifulSoup
from datetime import datetime
import discord
import requests
import pytz
import os


class Github(commands.Cog):
    '''Updates #githubs'''

    def __init__(self, bot):
        self.bot = bot
        self.update_github_embeds.start()

    def fetch_user_data(self, username):
        url = f'https://github.com/{username}'
        r = requests.get(url)
        if r.status_code != 200:
            return
        soup = BeautifulSoup(r.text, 'html.parser')
        info = soup.find_all('span', class_='text-bold color-text-primary')
        return {
            'name': soup.find('title').text.replace(' · GitHub', ''),
            'about': soup.find('div', class_='p-note user-profile-bio mb-3 js-user-profile-bio f4').text,
            'followers': info[0].text,
            'following': info[1].text,
            'starred': info[2].text,
            'repos': soup.find('span', class_='Counter').text,
            'url': url,
            'avatar': soup.find('a', attrs={'itemprop': 'image'})['href']
        }
        
    def embed_from_data(self, data):
        embed = discord.Embed(
            title=data['name'],
            type='rich',
            description=data['about'] if data['about'] else discord.Embed.Empty,
            url=data['url'],
            colour=0x277ecd
        )
        embed.set_thumbnail(url=data['avatar'])
        embed.add_field(
            name=f'👥 {data["followers"]} followers · {data["following"]} following · ⭐ {data["starred"]}',
            value=f'{data["repos"]} public repositories',
            inline=False
        )
        time = datetime.now(pytz.timezone('Asia/Tbilisi')).strftime("%Y-%m-%d · %H:%M:%S")
        embed.set_footer(
                text=f'Updated at: {time}',
                icon_url=discord.Embed.Empty
        )

        return embed
            
    @commands.command()
    async def github(self, ctx, username):
        '''Sends embed for GitHub user'''
        data = self.fetch_user_data(username)
        if data:
            embed = self.embed_from_data(data)
            embed.set_footer()
            await ctx.send(embed=embed)
        else:
            await ctx.send('User Not Found')

    @commands.command()
    async def addgithub(self, ctx, username):
        '''Creates embed for user in GITHUB_CHANNEL'''
        data = self.fetch_user_data(username)
        if data:
            embed = self.embed_from_data(data)
            github_channel = await self.bot.fetch_channel(os.environ['GITHUB_CHANNEL'])
            await github_channel.send(embed=embed)
        else:
            await ctx.send('User Not Found')
        
    @tasks.loop(hours=12.0)
    async def update_github_embeds(self):
        github_channel = await self.bot.fetch_channel(os.environ['GITHUB_CHANNEL'])
        messages = await github_channel.history(limit=20).flatten()
        for message in messages:
            if message.author == self.bot.user and len(message.embeds) == 1:
                username = message.embeds[0].title.split()[0]
                new_data = self.fetch_user_data(username)
                if not new_data:
                    await github_channel.send(f'Failed updating data for user: **{username}**')
                else:
                    new_embed = self.embed_from_data(new_data)
                    await message.edit(embed=new_embed)


def setup(bot):
    bot.add_cog(Github(bot))
