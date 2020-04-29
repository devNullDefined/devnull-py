import requests
import asyncio
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from datetime import datetime

with open('shiet.js', 'r') as f:
    shiet = f.read()


class Worldometer(commands.Cog):
    '''fuck your "Advanced Algorithm".'''
    current_proxy = ['', 0]  # ['proxy', 'times_used']
    url_home = 'https://www.worldometers.info/'
    url_corona = 'https://www.worldometers.info/coronavirus/'
    data = [{'title': 'Wordlometers', 'type': 'rich', 'color': 0x86c32a,
             'description': '0\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP} This Page',
             'footer': {'text': f'Updated at: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 'icon_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F692017015872167940%2F1fnJPzxM.png&f=1&nofb=1'}}]
    msg_id = 0
    
    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def check_current_proxy(cls):
        url = 'https://api.getproxylist.com/proxy?protocol=http'

        if cls.current_proxy[0] == '':
            r = requests.get(url)
        elif cls.current_proxy[1] == 10:
            r = requests.get(url, proxies={'http': cls.current_proxy[0]})
        else:
            return None
        cls.current_proxy[0] = f"http://{r.json()['ip']}:{r.json()['port']}"

    @classmethod
    def get_home_page(cls):
        cls.check_current_proxy()
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.http_proxy = cls.current_proxy[0]
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox.add_to_capabilities(capabilities)
    
        option = webdriver.ChromeOptions()
        option.add_argument('headless')

        driver = webdriver.Chrome(desired_capabilities=capabilities, options=option)
        driver.get(cls.url_home)
        cls.current_proxy[1] += 1
        return driver.execute_script(shiet)

    @commands.cooldown(1, 600, commands.BucketType.guild)
    @commands.command()
    async def worldometer(self, ctx):
        await ctx.send('gasasworebelia droebit ar mushaobs')
        return None
        msg = await ctx.send('**Retrieving data...**')
        page = self.get_home_page()
        groups = page.split('=')[1:]

        for i in range(len(groups)):
            listed = groups[i].split('|')
            group_title, counters = listed[0], listed[1:]
            self.data[0]['description'] += f'\n{i+1}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP} {group_title}'
            self.data.append({'title': group_title, 'type': 'rich', 'color': 0x86c32a, 'fields': [],
                              'footer': {'text': f'Updated at: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 'icon_url': 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpbs.twimg.com%2Fprofile_images%2F692017015872167940%2F1fnJPzxM.png&f=1&nofb=1'}})
            field = {}

            for j in range(len(counters)):
                if j % 2 == 0:
                    field['name'] = counters[j]
                else:
                    field['value'] = counters[j]
                    self.data[i+1]['fields'].append(field)
                    field = {}
        await msg.edit(content='', embed=discord.Embed.from_dict(self.data[0]))
        
        for i in range(len(self.data)):
            await msg.add_reaction(f'{i}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}')
        self.msg_id = msg.id

    @commands.Cog.listener('on_reaction_add')
    @commands.Cog.listener('on_reaction_remove')
    async def check_msg(self, reaction, user):
        if reaction.message.id == self.msg_id and user.id != self.bot.user.id:
            if str(reaction.emoji) == '0️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[0]))
            elif str(reaction.emoji) == '1️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[1]))
            elif str(reaction.emoji) == '2️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[2]))
            elif str(reaction.emoji) == '3️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[3]))
            elif str(reaction.emoji) == '4️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[4]))
            elif str(reaction.emoji) == '5️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[5]))
            elif str(reaction.emoji) == '6️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[6]))
            elif str(reaction.emoji) == '7️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[7]))
            elif str(reaction.emoji) == '8️⃣':
                await reaction.message.edit(embed=discord.Embed.from_dict(self.data[8]))

    @worldometer.error
    async def worldometer_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Command on cooldown. Try again in {round(error.retry_after)} seconds')


def setup(bot):
    bot.add_cog(Worldometer(bot))
