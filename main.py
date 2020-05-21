import os

from discord.ext import commands

from Bombola import Bombola
from Description import Description

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
bot.remove_command('list')
guild_id = os.getenv('GUILD_ID')

if __name__ == '__main__':
    bot.add_cog(Bombola(bot, guild_id))
    bot.add_cog(Description(bot))
    bot.run(TOKEN)
