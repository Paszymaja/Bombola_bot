import datetime
import json
import random
import markovify
import os
import pyAesCrypt

from discord.ext import commands, tasks


class ServerUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_data = json.load(open('data/id/id.json', 'r'))
        self.thoughts_id = self.config_data['thoughts_id']
        self.main_channel_id = self.config_data['main_channel_id']
        self.daily_thoughts.start()
        self.messages = []
        # Markov chain variables
        self.enc_key = os.getenv('ENC_KEY')
        pyAesCrypt.decryptFile('data/messages/messages.txt', 'temp/data_out.txt', self.enc_key, bufferSize=10 * 1024)
        self.chain_data = json.load(open('temp/data_out.txt', 'r', encoding='utf-8'))
        self.text_model = markovify.Text(' '.join(self.chain_data))

    def cog_unload(self):
        self.daily_thoughts.cancel()

    @tasks.loop(minutes=1)
    async def daily_thoughts(self):
        send_channel = self.bot.get_channel(self.main_channel_id)
        if datetime.datetime.now().hour == 12 and datetime.datetime.now().minute == 0:
            ctx_message = f'Srebrna myśl na dziś\n {random.choice(self.messages)}'
            print(ctx_message)
            await send_channel.send(ctx_message)

    @daily_thoughts.before_loop
    async def before_daily_thoughts(self):
        print('daily thoughts loop waiting ...')
        await self.bot.wait_until_ready()
        print('rdy')
        channel = self.bot.get_channel(self.thoughts_id)
        messages = await channel.history(limit=200).flatten()
        self.messages = [message.content for message in messages]

    @commands.command(name='tekst', help='Markov Chain do rozmowy.')
    async def chain(self, ctx):
        if (chain := self.text_model.make_sentence()) is None:
            ctx_message = 'Coś poszło nie tak. Spróbuj jeszcze raz.'
        else:
            ctx_message = chain
        print(ctx_message)
        await ctx.channel.send(ctx_message)
