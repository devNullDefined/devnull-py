import random
import discord
from discord.ext import tasks, commands


class Playlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_channel = bot.get_channel(617702259282935808)
        self.listen.start()

    def get_music_title(self, messages):
        random_message = random.choice(messages)
        if random_message.embeds:
            return random_message.embeds[0].to_dict()['title']
        self.get_music_title(messages)

    @tasks.loop(minutes=5.0)
    async def listen(self):
        messages = await self.music_channel.history(limit=200).flatten()
        title = self.get_music_title(messages)
        listening = discord.Activity(type=discord.Activity.listening, name=title)
        await bot.change_presence(activity=listening)


def setup(bot):
    bot.add_cog(Playlist(bot))
