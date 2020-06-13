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
        pass

    @daily_thoughts.before_loop
    async def before_daily_thoughts(self):
        print('daily thoughts loop waiting ...')
        await self.bot.wait_until_ready()
        print('rdy')
        channel = self.bot.get_channel(207553209038798849)
        messages = await channel.history(limit=200).flatten()
        print(messages)
