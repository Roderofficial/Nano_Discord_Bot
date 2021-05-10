from discord.ext import commands
import mysql.connector
import discord
import settings
from datetime import datetime
from addons.setting_download import *
import asyncio
#todo: dodać najnowszego użytkownika
#todo: dodać rekord online

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def get_and_update_record_online(self, gid, online):
        #print(gid)
        #print(online)

        # select do bazy

        gid = str(gid)
        online = str(online)
        #print('connect')
        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()
        sql = "SELECT record FROM `record_online` WHERE gid = %s"
        mycursor.execute(sql, (gid,))
        myresult = mycursor.fetchone()

        #print(myresult)

        #sprawdzenie czy warunek instnieje
        if myresult is None:
            #stworzenie pierwszego rekordu
            gid = str(gid)
            online = str(online)
            #print('Is none')
            sql = "INSERT INTO `record_online` (`gid`, `record`) VALUES (%s, %s) "
            mycursor.execute(sql, (gid, online))
            mydb.commit()
            return online
        else:
            #konwersja do int

            online = int(online)
            count_from_database = int(myresult[0])
            if online > count_from_database:
                #zaktualizowanie nowego rekordu użytkowników
                #print('else none')
                sql = "UPDATE `record_online` SET `record` = %s WHERE `record_online`.`gid` = %s"
                mycursor.execute(sql, (online, gid))
                mydb.commit()
                return online
            else:
                #zwrocenie rekordu z bazy który był większy
                return count_from_database


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

        #online status update
        record_channel = self.bot.get_channel(data['member_record_channel_id'])
        record_count = await self.get_and_update_record_online(guild_id, online_count)
        new_name = f"{data['member_record_prefix']} {record_count} {data['member_record_suffix']}"
        await record_channel.edit(name=new_name)

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
    async def tca(self,ctx, count):
        print('record:')
        print(self.get_and_update_record_online(ctx.guild.id, count))

    @commands.Cog.listener()
    async def on_ready(self):
        print("---MODULE STATS RUNNING---")
        await self.update_all()

