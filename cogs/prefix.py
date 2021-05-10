from addons.setting_download import *
from discord.ext import commands
import discord
import settings
import mysql.connector

class prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        mention = f'<@!{self.bot.user.id}>'
        if mention == message.content:
            await message.channel.send(f"🔗 Cześć, mój prefix to: ``{get_prefix(self, message)}``. Jeśli potrzebujesz wiecej informacji odwiedź naszą stronę https://nanodc.xyz")



#setup
def setup(self):
    print("Moduł cogs.admin załadowany!")

def get_prefix(self, ctx):
    default_prefixes = '>'
    data = download_settings(ctx.guild.id, "global")
    # Only allow custom prefixs in guild
    try:
        if data['prefix'] is not None:

            #print(data['prefix'])
            return data['prefix']
        else:
            print(default_prefixes)
            return  default_prefixes
    except:
        return default_prefixes
