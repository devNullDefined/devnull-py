import os
import discord
import requests
from discord.ext import tasks, commands
from requests.auth import HTTPBasicAuth


class Github(commands.Cog):
    '''Updates #githubs'''

    def __init__(self, bot):
        self.bot = bot
        self.auth = HTTPBasicAuth(os.environ['GITHUB_USER'], os.environ['GITHUB_PAS'])
        self.update_github_embeds.start()

    def fetch_user_data(self, username):
        r = requests.get(f'https://api.github.com/users/{username}', auth=self.auth)
        if r.status_code == 404:
            return None
        return r.json()

    def embed_from_data(self, data):
        name = data['login']
        r = requests.get(f'https://api.github.com/users/{name}/starred', auth=self.auth)
        if r.headers.get('Link'):
            last_page = re.findall(r'\d+', r.headers['Link'])[-1]
            rl = requests.get(f'https://api.github.com/users/{name}/starred?page={last_page}', auth=self.auth)
            starred = (int(last_page)-1) * 30 + len(rl.json())
        else:
            starred = len(r.json())
        
        updated_at = data['updated_at'].replace('T', ' · ')[:-1]

        if data['name']:
            name = f'{data["name"]} · {name}'

        embed = discord.Embed(
            title=name,
            type='rich',
            description=data['bio'] if data['bio'] else discord.Embed.Empty,
            url=data['html_url'],
            colour=0x277ecd
        )
        embed.set_thumbnail(url=data['avatar_url'])
        embed.add_field(
            name=f'👥 {data["followers"]} followers · {data["following"]} following · ⭐ {starred}',
            value=f'{data["public_repos"]} public repositories',
            inline=False
        )
        embed.set_footer(
                text=f'Updated at: {updated_at}',
                icon_url=discord.Embed.Empty
        )

        return embed
        
    @commands.command()
    async def github(self, ctx, username):
        '''Send embed for GitHub user'''
        data = self.fetch_user_data(username)
        if data:
            embed = self.embed_from_data(data)
            embed.set_footer()
            await ctx.send(embed=embed)
        else:
            await ctx.send('User Not Found')

    @commands.command()
    async def addgithub(self, ctx, username):
        '''Create embed for user in GITHUB_CHANNEL'''
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
                embed_dict = message.embeds[0].to_dict()
                update_timestamp = embed_dict['footer']['text'].split(': ')[1].replace(' · ', 'T') + 'Z'
                username = embed_dict['url'].split('/')[-1]
                new_data = self.fetch_user_data(username)
                if not new_data:
                    await github_channel.send(f'Failed updating data for user: **{username}**')
                else:
                    if new_data['updated_at'] != update_timestamp:
                        new_embed = self.embed_from_data(new_data)
                        await message.edit(embed=new_embed)


def setup(bot):
    bot.add_cog(Github(bot))
