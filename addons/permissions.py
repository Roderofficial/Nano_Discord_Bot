from discord.ext import commands
import mysql.connector
import discord
import settings
from datetime import datetime
from addons.setting_download import *
import asyncio


class permissions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    @commands.group(name="permissions",aliases=['per'])
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        print("Permission Command")






