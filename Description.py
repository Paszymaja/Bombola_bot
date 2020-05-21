from itertools import cycle

import discord
from discord.ext import commands, tasks


class Description(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status = ['Pizza', 'Bombola', 'Sycylijska', '🍕']
        self.change_status.start()
        self.msgs = cycle(self.status)

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(minutes=10)
    async def change_status(self):
        current_status = next(self.msgs)
        await self.bot.change_presence(activity=discord.Game(name=current_status))

    @change_status.before_loop
    async def before_timer(self):
        print('Status loop waiting... ')
        await self.bot.wait_until_ready()
        print('rdy')
