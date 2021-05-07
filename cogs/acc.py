from discord.ext import commands
import mysql.connector
import discord
import settings
from datetime import datetime
from addons.setting_download import *
import asyncio


class acc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

