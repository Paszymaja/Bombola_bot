import datetime
import json
import os
import random

import asyncpg
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
from twilio.rest import Client

from cogs import Delivery


def price_check(index):
    pizza_name, pizza_price = [], []
    url = 'https://www.pizzeriabombola.pl/menu.php'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    table = soup.find_all('div', attrs={'style': 'float: right; width: 450px; margin-top:5px;'})

    for pizza in table:
        pizza_name = pizza.find_all('strong')
        pizza_price = pizza.find_all('td', class_='t3b')

    return pizza_name[index].text, pizza_price[index].text


def load_list():
    review_list = []
    for counter, entry in enumerate(os.listdir('data/review')):
        if os.path.isfile(os.path.join('data/review', entry)):
            with open(f'data/review/{counter}.txt', encoding='utf-8') as fp:
                review_list.append(fp.read().splitlines())
    return review_list


class Bombola(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_data = json.load(open('data/id/id.json', 'r'))
        self.main_channel_id = self.config_data['main_channel_id']
        self.last_price = price_check(index=0)[1][:-3]
        self.timer.add_exception_type(asyncpg.PostgresConnectionError)
        self.timer.start()
        self.last_date = datetime.datetime.strptime(os.getenv('LAST_DATE'), '%Y %m %d')
        self.image_url = 'https://www.pizzeriabombola.pl/images/dowoz.jpg'
        self.review_list = load_list()
        # variables used for calling
        self.account_sid = os.getenv('ACC_SID')
        self.auth_token = os.getenv('CALL_TOKEN')
        self.szymek_number = os.getenv('SZYMEK_NUMBER')

    def cog_unload(self):
        self.timer.cancel()

    @commands.command(name='cena', help='Aktualna cena pizzy w bomboli.')
    async def price(self, ctx, index: int = 0):
        pizza_name, pizza_price = price_check(index)

        ctx_message = f'Cena {pizza_name} to {pizza_price}.'

        print(ctx_message)
        await ctx.send(ctx_message)

    @commands.command(name='dostawa', help='Cena dostawy.')
    async def order(self, ctx):
        image = Delivery.get_image(self.image_url)

        ctx_message = f'Cena dostawy to {Delivery.delivery(image)[0]} zł.'

        print(ctx_message)
        await ctx.send(ctx_message)

    @commands.command(name='czas', help='Czas od ostatniej zmiany ceny bomboli.')
    async def time(self, ctx):
        date_object = datetime.datetime.now()
        elapsed_time = date_object - self.last_date
        days = elapsed_time.days

        ctx_message = f'Od ostatniej zmiany ceny upłyneło {days} dni.'

        print(ctx_message)
        await ctx.send(ctx_message)

    @commands.command(name='recenzja', help='Generowana recenzja.')
    async def review(self, ctx):
        review_text = [random.choice(self.review_list[index]) for index in range(3)]

        ctx_message = " ".join(review_text)

        print(ctx_message)
        await ctx.channel.send(ctx_message)

    @commands.command(name='szymek', help='Zadzwoń do szymka.')
    @commands.cooldown(1, 3000, commands.BucketType.default)  # 50 min in sec
    async def call(self, ctx):
        client = Client(self.account_sid, self.auth_token)
        if 10 < datetime.datetime.now().hour < 23:
            client.calls.create(url='https://github.com/Paszymaja/'
                                    'Bombola_bot/blob/master/data/call_response/voice.xml',
                                from_='+12568010578',
                                to=self.szymek_number)
            ctx_message = 'dzwonione.'
        else:
            ctx_message = 'Szymek śpi. 😴'

        print(ctx_message)
        await ctx.channel.send(ctx_message)

    @call.error
    async def call_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            ctx_message = f'Nie możesz teraz zadzwonić do Szymka. Spróbuj za {error.retry_after / 60:.0f} min.'

            print(ctx_message)
            await ctx.send(ctx_message)
        else:
            raise error

    @tasks.loop(minutes=30)
    async def timer(self):
        current_price = price_check(index=0)[1][:-3]
        if current_price != self.last_price:
            print('Cena się zmieniła.')
            self.timer.stop()
        else:
            print('Cena się nie zmieniła.')

    @timer.before_loop
    async def before_timer(self):
        print('Bombola loop waiting...')
        await self.bot.wait_until_ready()
        print('rdy')

    @timer.after_loop
    async def after_timer(self):
        await self.price_change()

    @commands.Cog.listener()
    async def price_change(self):
        channel = self.bot.get_channel(self.main_channel_id)
        await channel.send('@here Zmiana ceny!!!!')
        self.last_price = price_check(index=0)[1][:-3]
        self.last_date = datetime.datetime.now()
        self.timer.start()  # restart timer
