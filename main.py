import os
import requests
import datetime

from bs4 import BeautifulSoup
from discord.ext import commands, tasks

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
bot.remove_command('list')


@bot.command(name='cena', help='Aktualna cena pizzy w bomboli')
async def price(ctx, index: int = 0):
    pizza_name, pizza_price = [], []
    url = 'https://www.pizzeriabombola.pl/menu.php'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('div', attrs={'style': 'float: right; width: 450px; margin-top:5px;'})

    for pizza in table:
        pizza_name = pizza.find_all('strong')
        pizza_price = pizza.find_all('td', class_='t3b')

    ctx_message = f'Cena {pizza_name[index].text} to {pizza_price[index].text}'

    print(ctx_message)
    await ctx.send(ctx_message)


@bot.command(name='czas', help='czas od ostatniej zmiany ceny bomboli')
async def time(ctx):
    date_object = datetime.datetime.now()
    last_date = datetime.datetime.strptime(os.getenv('LAST_DATE'), '%Y %m %d')
    elapsed_time = date_object - last_date
    days = elapsed_time.days

    ctx_message = f'Od ostatniej zmiany ceny upłyneło {days} dni'

    print(ctx_message)
    await ctx.send(ctx_message)


@tasks.loop(seconds=30)
async def price_check():  # TODO sprawdzanie zmian ceny
    pass


if __name__ == '__main__':
    price_check.start()
    bot.run(TOKEN)
