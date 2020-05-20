import datetime
import os

import asyncpg
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks


def price_check(index):
    pizza_name, pizza_price = [], []
    url = 'https://www.pizzeriabombola.pl/menu.php'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('div', attrs={'style': 'float: right; width: 450px; margin-top:5px;'})

    for pizza in table:
        pizza_name = pizza.find_all('strong')
        pizza_price = pizza.find_all('td', class_='t3b')

    return pizza_name[index].text, pizza_price[index].text


class Bombola(commands.Cog):
    def __init__(self, bot, guild_id):
        self.last_price = price_check(index=0)[1][:-3]
        self.bot = bot
        self.timer.add_exception_type(asyncpg.PostgresConnectionError)
        self.timer.start()
        self.guild_id = guild_id

    def cog_unload(self):
        self.timer.cancel()

    @commands.command(name='cena', help='Aktualna cena pizzy w bomboli')
    async def price(self, ctx, index: int = 0):
        pizza_name, pizza_price = price_check(index)

        ctx_message = f'Cena {pizza_name} to {pizza_price}'

        print(ctx_message)
        await ctx.send(ctx_message)

    @commands.command(name='czas', help='czas od ostatniej zmiany ceny bomboli')
    async def time(self, ctx):
        date_object = datetime.datetime.now()
        last_date = datetime.datetime.strptime(os.getenv('LAST_DATE'), '%Y %m %d')
        elapsed_time = date_object - last_date
        days = elapsed_time.days

        ctx_message = f'Od ostatniej zmiany ceny upłyneło {days} dni'

        print(ctx_message)
        await ctx.send(ctx_message)

    @tasks.loop(minutes=10)
    async def timer(self):
        current_price = price_check(index=0)[1][:-3]
        if current_price != self.last_price:
            print('Cena się zmieniła')
            self.timer.stop()
        else:
            print('Cena się nie zmieniła')

    @timer.before_loop
    async def before_timer(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    @timer.after_loop
    async def after_timer(self):
        await self.price_change()

    @commands.Cog.listener()
    async def price_change(self):
        guild = self.bot.get_guild(self.guild_id)
        channel = guild.text_channels[0]
        await channel.send('@here Zmiana ceny!!!!')
        self.last_price = price_check(index=0)[1][:-3]
