import os
import requests

from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name='cena', help='Aktualna cena pół bomboli pół sycylijskiej')
async def nine_nine(cena):
    name, price = [], []
    url = 'https://www.pizzeriabombola.pl/menu.php'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('div', attrs={'style': 'float: right; width: 450px; margin-top:5px;'})

    for pizza in table:
        name = pizza.find_all('strong')
        price = pizza.find_all('td', class_='t3b')

    await cena.send(f'Cena {name[0].text} to {price[0].text}')

bot.run(TOKEN)
