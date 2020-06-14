import datetime
import random

from discord.ext import commands, tasks


class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.thoughts_id = 207553209038798849
        self.bot_development_id = 715172222205165629
        self.daily_thoughts.start()
        self.messages = []

    def cog_unload(self):
        self.daily_thoughts.cancel()

    @tasks.loop(hours=1)
    async def daily_thoughts(self):
        send_channel = self.bot.get_channel(self.bot_development_id)
        if datetime.datetime.now().hour == 12:
            ctx_message = f'Srebrna myśl na dziś\n {random.choice(self.messages)}'
            print(ctx_message)
            await send_channel.send(ctx_message)
        else:
            print('hour loop')

    @daily_thoughts.before_loop
    async def before_daily_thoughts(self):
        print('daily thoughts loop waiting ...')
        await self.bot.wait_until_ready()
        print('rdy')
        channel = self.bot.get_channel(self.thoughts_id)
        messages = await channel.history(limit=200).flatten()
        self.messages = [message.content for message in messages]
