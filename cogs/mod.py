from discord.ext import commands
import discord
import os


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, new_prefix):
        os.environ['PREFIX'] = new_prefix
        await ctx.send(f'New Prefix set: `{new_prefix}`')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, limit: int, user: discord.Member=None):
        if amount < 1:
            await ctx.send('Min amount = 1')
            return
        if amount > 100:
            await ctx.send('Max amount = 100')
            return

        if not user:
            try:
                await ctx.channel.purge(limit=amount+1)
            except Exception as e:
                await ctx.send(e)
            return

        if user == ctx.author:
            amount += 1

        messages_to_delete = []
        while True:
            async for message in ctx.channel.history():
                if amount == 0:
                    try:
                        await ctx.channel.delete_messages(messages_to_delete)
                    except Exception as e:
                        await ctx.send(e)
                    return
                if message.author == user:
                    messages_to_delete.append(message)
                    amount -= 1


def setup(bot):
    bot.add_cog(Mod(bot))
