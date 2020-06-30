import os

from discord.ext import commands

from cogs.Bombola import Bombola
from cogs.Description import Description
from cogs.ServerUtils import ServerUtils

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

if __name__ == '__main__':
    bot.add_cog(Bombola(bot))
    bot.add_cog(Description(bot))
    bot.add_cog(ServerUtils(bot))
    bot.run(TOKEN)
