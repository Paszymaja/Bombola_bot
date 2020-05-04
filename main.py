import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "!bombola":
        response = "Bombola"
        await message.channel.send(response)
    elif message.content == "raise-exception":
        raise discord.DiscordException

client.run(TOKEN)
