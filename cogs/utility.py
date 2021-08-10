from discord.ext import commands
import discord


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'pong: {round(self.bot.latency * 1000)}MS')

    @commands.command()
    async def emoji(self, ctx, *names):
        '''Sends any emoji from any server bot is connected to (No Nitro Required)'''
        converter = commands.EmojiConverter()
        content = ''
        for name in names:
            emoji = await converter.convert(ctx, name)
            content += str(emoji)
        await ctx.send(content)

    @commands.command()
    async def react(self, ctx, msg_id, *names):
        '''Reacts with any emoji from any server bot is connected to (No Nitro Required)'''
        converter = commands.EmojiConverter()
        msg = await ctx.fetch_message(msg_id)
        for name in names:
            emoji = await converter.convert(ctx, name)
            await msg.add_reaction(emoji)

    @commands.command()
    async def commands(self, ctx, group=None):
        if group:
            cog = self.bot.get_cog(group.capitalize())
            if not cog:
                await ctx.send('Group not found')
                return
            msg = '```asciidoc'
            sep = len(max([command.name for command in cog.get_commands()], key=len)) + 2
            for command in cog.get_commands():
                msg += f'\n• {command.name}{" " * (sep-len(command.name))}:: {command.help if command.help else ""}'
            msg += f'```\nUse `{ctx.prefix}help <command>`for help with specific command'
            await ctx.send(msg)
        else:
            embed = discord.Embed(
                title='List of Command Groups',
                type='rich',
                description=f'To view the commands in each group use:\n```{ctx.prefix}commands <group>```',
                colour=0x3172d9
            )
            for cog in self.bot.cogs:
                embed.add_field(
                    name=f'**{cog}**',
                    value=f'{len(self.bot.get_cog(cog).get_commands())} commands'
                )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
