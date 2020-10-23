import os
import random
import discord
from discord.ext import tasks, commands


class Playlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.listen.start()

    def get_music_title(self, messages):
        random_message = random.choice(messages)
        try:
            return random_message.embeds[0].to_dict()['title']
        except:
            return self.get_music_title(messages)

    @tasks.loop(minutes=5.0)
    async def listen(self):
        music_channel = await self.bot.fetch_channel(os.environ['MUSIC_CHANNEL'])
        messages = await music_channel.history(limit=200).flatten()
        title = self.get_music_title(messages)
        listening = discord.Activity(type=discord.ActivityType.listening, name=title)
        await self.bot.change_presence(activity=listening)


def setup(bot):
    bot.add_cog(Playlist(bot))
