from discord.ext import commands
import discord
import settings
import mysql.connector
from datetime import datetime
from addons.setting_download import download_settings
import re


class licence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('- Sprawdzanie licencji -')
        for guild in self.bot.guilds:
            print(guild.id)



# setup
def setup(self):
    print("Moduł cogs.mute załadowany!")
