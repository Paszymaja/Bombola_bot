import os

from discord.ext import commands

from Bombola import Bombola

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
bot.remove_command('list')
guild_id = 205741964740657153

if __name__ == '__main__':
    bot.add_cog(Bombola(bot, guild_id))
    bot.run(TOKEN)
