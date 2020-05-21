import os

from discord.ext import commands

from cogs.Bombola import Bombola
from cogs.Description import Description

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
bot.remove_command('list')

if __name__ == '__main__':
    bot.add_cog(Bombola(bot))
    bot.add_cog(Description(bot))
    bot.run(TOKEN)
