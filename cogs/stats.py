from discord.ext import commands
import mysql.connector
import discord
import settings
from datetime import datetime
from addons.setting_download import *
import asyncio


class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    #member online count
    async def get_member_online(self, ctx, guild_id):
        #counter
        count = 0
        #get guild
        guild = self.bot.get_guild(guild_id)

        #loop counting
        for a in guild.members:
            if a.status.value != 'offline':
                count = count + 1

        return count


    #member count
    async def get_member_count(self, ctx, guild_id):
        #counter
        count = 0
        #get guild
        guild = self.bot.get_guild(guild_id)

        #loop counting
        for a in guild.members:
                count = count + 1

        return count

    #member ban list
    async def member_ban_count(self, ctx, guild_id):
        # get guild
        guild = self.bot.get_guild(guild_id)

        #get banlist
        banlist = await guild.bans()

        #counter
        count = 0

        #loop counter
        for a in banlist:
            count = count +1
        return count

    async def update_status_server(self, guild_id):
        data = download_settings(guild_id, "stats")
        try:
            enable = data['enable']
        except:
            enable = 0
        if enable != 1:
            return 0

        #online status update
        online_channel = self.bot.get_channel(data['member_online_count_channel_id'])
        online_count = await self.get_member_online(None, guild_id)
        new_name = f"{data['member_online_count_prefix']} {online_count} {data['member_online_count_suffix']}"
        await online_channel.edit(name=new_name)

        # bans status update
        ban_channel = self.bot.get_channel(data['member_ban_count_channel_id'])
        ban_count = await self.member_ban_count(None, guild_id)
        new_name = f"{data['member_ban_count_prefix']} {ban_count} {data['member_ban_count_suffix']}"
        await ban_channel.edit(name=new_name)

        # count status update
        count_channel = self.bot.get_channel(data['member_count_channel_id'])
        all_count = await self.get_member_count(None, guild_id)
        new_name = f"{data['member_count_prefix']} {all_count} {data['member_count_suffix']}"
        await count_channel.edit(name=new_name)

        print(f'Updated id: {guild_id}')

    async def update_all(self):
        while True:
            print('------UPDATE ALL-----')
            mydb = mysql.connector.connect(
                host=settings.db_adres,
                user=settings.db_login,
                password=settings.db_password,
                database=settings.db_base
            )
            mycursor = mydb.cursor()
            sql = "SELECT dc_guild_id FROM bot_server_settings WHERE module_name = 'stats'"
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
            mycursor.close()
            mydb.close()
            for a in myresult:
                if a[0] is not None:
                    await self.update_status_server(int(a[0]))
            await asyncio.sleep(60)


    @commands.command()
    async def tc(self,ctx):
        await self.update_all()

    @commands.Cog.listener()
    async def on_ready(self):
        print("---MODULE STATS RUNNING---")
        await self.update_all()

