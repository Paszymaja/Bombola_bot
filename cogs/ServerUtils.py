import datetime
import json
import random

from discord.ext import commands, tasks


class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_data = json.load(open('data/id/id.json', 'r'))
        self.thoughts_id = self.config_data['thoughts_id']
        self.bot_development_id = self.config_data['bot_development_id']
        self.daily_thoughts.start()
        self.messages = []

    def cog_unload(self):
        self.daily_thoughts.cancel()

    @tasks.loop(minutes=1)
    async def daily_thoughts(self):
        send_channel = self.bot.get_channel(self.bot_development_id)
        if datetime.datetime.now().hour == 12 and datetime.datetime.now().minute == 0:
            ctx_message = f'Srebrna myśl na dziś\n {random.choice(self.messages)}'
            print(ctx_message)
            await send_channel.send(ctx_message)
        else:
            print(f'hour loop {datetime.datetime.now().hour}')

    @daily_thoughts.before_loop
    async def before_daily_thoughts(self):
        print('daily thoughts loop waiting ...')
        await self.bot.wait_until_ready()
        print('rdy')
        channel = self.bot.get_channel(self.thoughts_id)
        messages = await channel.history(limit=200).flatten()
        self.messages = [message.content for message in messages]
