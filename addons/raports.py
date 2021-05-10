from addons.setting_download import *
from discord.ext import commands
import discord
import settings
import mysql.connector
from datetime import datetime
import asyncio

class raport(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def update_raport(self, gid):
        #obecny czas
        czas = datetime.now()

        #get members status
        #all
        all = 0

        #online
        online = 0

        #dnd
        dnd = 0

        #idle
        idle = 0

        #offline
        offline = 0

        #mobile_status
        mobile_status = 0

        #web_status
        web_status = 0

        #desktop_status
        desktop_status = 0

        #users status
        guild = self.bot.get_guild(gid)
        for a in guild.members:
            all = all + 1
            #check status
            if a.status.value == "online":
                online = online + 1
            elif a.status.value == "dnd":
                dnd = dnd + 1
            elif a.status.value == "idle":
                idle = idle + 1
            elif a.status.value == "offline":
                offline = offline + 1

            #count devices
            if a.mobile_status.value != "offline":
                mobile_status = mobile_status + 1
            if a.web_status.value != "offline":
                web_status = web_status + 1
            if a.desktop_status.value != "offline":
                desktop_status = desktop_status + 1

        #channel count types and voice members
        #voice channel member counts
        vc_mebers_count = 0

        #voice channel count
        vc_count = 0

        #text channel count
        tc_count = 0
        #get list channel
        for a in guild.channels:

            #check channel type
            if a.type.name == "voice":
                vc_count = vc_count + 1
                for b in a.members:
                    #member on voice channel count
                    vc_mebers_count = vc_mebers_count + 1
            elif a.type.name == "text":
                tc_count = tc_count + 1


        #ban count
        ban_count = 0
        banlist = await guild.bans()
        for a in banlist:
            ban_count = ban_count + 1


        #print(f"All: {all}")
        #print(f"Online: {online}")
        #print(f"Dnd: {dnd}")
        #print(f"Idle: {idle}")
        #print(f"Offline: {offline}")
        #print(f"Voice channels count: {vc_count}")
        #print(f"Text channel count: {tc_count}")
        #print(f"Voice channel members: {vc_mebers_count}")
        #print(f"Ban count: {ban_count}")
        #print(f"Mobile status: {mobile_status}")
        #print(f"Web status: {web_status}")
        #print(f"Computer status: {desktop_status}")



        tablica = {}
        tablica['all'] = all
        tablica['online'] = online
        tablica['dnd'] = dnd
        tablica['idle'] = idle
        tablica['offline'] = offline
        tablica['vc_count'] = vc_count
        tablica['tc_count'] = tc_count
        tablica['vc_members_count'] = vc_mebers_count
        tablica['ban_count'] = ban_count
        tablica['mobile_status'] = mobile_status
        tablica['web_status'] = web_status
        tablica['desktop_status'] = desktop_status

        json_table = json.dumps(tablica)
        #print(json_table)


        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO `raports` (`gid`, `datetime`, `data`) VALUES (%s, %s, %s)"
        val = (gid,czas,json_table)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    async def update_all(self):
        while True:
            print('------UPDATE RAPORTS-----')
            for guild in self.bot.guilds:
                await self.update_raport(guild.id)

            await asyncio.sleep(300)


    @commands.Cog.listener()
    async def on_ready(self):
        print("---MODULE RAPORT RUNNING---")
        await self.update_all()

    @commands.is_owner()
    @commands.command()
    async def tca(self,ctx):
        print('update')
        await self.update_raport(ctx.guild.id)



#setup
def setup(self):
    print("Moduł cogs.admin załadowany!")