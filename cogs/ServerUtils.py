import os

from discord.ext import commands, tasks


class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = os.getenv('GUILD_ID')
        self.daily_thoughts.start()

    def cog_unload(self):
        self.daily_thoughts.cancel()

    @tasks.loop(seconds=3)
    async def daily_thoughts(self):
        guild = self.bot.get_guild(self.guild_id)
        channel = guild.text_channels[0]
        print(channel)
