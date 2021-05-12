from discord.ext import commands
import discord
import settings
import mysql.connector
from addons.setting_download import *
import asyncio
from discord.utils import get
from datetime import datetime, timedelta

class mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    #temp mute insert to database
    async def database_add(self, aiotid, gid, member_id, expire_time):
        """
        :param aiotid: Async_io task id
        :param gid: Discord guild id
        :param member_id: Discord member id
        :param expire_time: Expire time in datetime
        :return: Nothing
        """

        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO `mute` (`id`, `async_task_id`, `gid`, `member_id`, `expire_time`) VALUES (NULL, %s, %s, %s, %s) "
        val = (aiotid, gid, member_id, expire_time)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    # temp mute remove from
    async def database_remove(self, aiotid):
        """
        :param aiotid: Async_io task id
        :return: Nothing
        """

        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()

        sql = "DELETE FROM `mute` WHERE `async_task_id` = %s"
        val = (aiotid,)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    #time convert
    def convert_time_to_seconds(self,time):
        time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            return int(time[:-1]) * time_convert[time[-1]]
        except:
            return None

    #async task for tempmute
    async def temp_mute_task(self, ctx, member, time, *reason):
        """

        :param ctx: Context
        :param member: Discord member
        :param time: Time, example: 1d, 1h, 1m, 1s
        :param reason: Reason for mute *optional*
        :return: Nothing
        """


        #reason chceck
        if len(reason[0]) == 0:
            reason = "Brak"
        else:
            reason = " ".join(reason[:])

        #get guild and other data
        guild_id = str(ctx.guild.id)
        data = download_settings(guild_id, "mute")
        role = get(ctx.guild.roles, id=data['role_id'])

        #time and converts
        converted_time = self.convert_time_to_seconds(time)

        #check time
        if converted_time is None:
            await ctx.channel.send("Podano niepoprawny czas!")
            return None

        #check if muted
        if role in member.roles:
            await ctx.channel.send('Ten użytkownk jest już wyciszony')
            return None

        #converts
        datetime_end = datetime.now() + timedelta(seconds=converted_time)
        czas_czytelny = datetime_end.strftime("%d/%m/%Y %H:%M:%S")

        #asyncio task rename
        task = asyncio.current_task()
        task.set_name(str(ctx.message.id))
        task_id = ctx.message.id

        #add to database
        await self.database_add(task_id, guild_id,member.id,datetime_end)

        #embed message for channel
        embed = discord.Embed(description=f"Powód: {reason} \nCzas: {time} \nWygasa: {czas_czytelny} \nPrzez:{ctx.author}", color=0xfff904)
        embed.set_author(name=f"Wyciszono użytkownika: {member}", icon_url=member.avatar_url)
        embed.set_footer(text=f"Mute id: {ctx.message.id}")

        #embed message for DM
        dm = discord.Embed(description=f"Powód: {reason} \nCzas: {time} \nWygasa: {czas_czytelny} \nPrzez:{ctx.author}", color = 0xfff904)
        dm.set_author(name=f"Wyciszono cię na serwerze: {ctx.guild}",
                         icon_url=ctx.guild.icon_url)
        dm.set_footer(text=f"Mute id: {ctx.message.id}")

        #add mute role
        await ctx.channel.send(embed=embed)
        await member.send(embed=dm)
        await member.add_roles(role)

        #sleep
        await asyncio.sleep(int(converted_time))

        #remove role
        await member.remove_roles(role)
        await self.database_remove(task_id)

    #aync recovery auto unmute
    async def recovery_unmute(self, task):
        #data
        guild = self.bot.get_guild(int(task[2]))
        guild_id = str(task[2])
        data = download_settings(guild_id, "mute")
        role = get(guild.roles, id=data['role_id'])
        member = guild.get_member(int(task[3]))
        timenow = datetime.now()
        name_task = task[1]
        print(member)
        if role not in member.roles:
            await self.database_remove(name_task)
            print('Mute anolowany')
            return None

        if task[4] < timenow:
            await member.remove_roles(role)
            await self.database_remove(task[1])

        else:
            left_time = task[4] - timenow
            time_to_second = int(left_time.total_seconds())
            print(time_to_second)

            # asyncio task rename
            task = asyncio.current_task()
            task.set_name(name_task)

            # sleep
            await asyncio.sleep(int(time_to_second))

            await member.remove_roles(role)
            await self.database_remove(name_task)



    #system recovery after stop
    async def recover_system(self):
        #db connect
        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()

        sql = "SELECT * FROM `mute`"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()

        for a in myresult:
            await self.recovery_unmute(a)







    #tempmute command
    @commands.command(name="tempmute")
    @commands.has_permissions(kick_members=True)
    async def tempmute(self, ctx, member: discord.Member, time, *reason):
        await self.temp_mute_task(ctx, member,time,reason)


    #mute command
    @commands.command(name="mute")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, *reason):
        #check reason
        if reason:
            if len(reason[0]) == 0:
                reason = "Brak"
            else:
                reason = " ".join(reason[:])
        else:
            reason = "Brak"
        #get guild and other data
        guild_id = str(ctx.guild.id)
        data = download_settings(guild_id, "mute")
        role = get(ctx.guild.roles, id=data['role_id'])

        #check role
        if role in member.roles:
            await ctx.channel.send('Ten użytkownk jest już wyciszony')
            return None

        #embed message for channel
        embed = discord.Embed(description=f"Powód: {reason} \nCzas: ∞ \nWygasa: Nigdy \nPrzez:{ctx.author}", color=0xfff904)
        embed.set_author(name=f"Wyciszono użytkownika: {member}", icon_url=member.avatar_url)
        embed.set_footer(text=f"Mute id: {ctx.message.id}")

        #embed message for DM
        dm = discord.Embed(description=f"Powód: {reason} \nCzas: ∞ \nWygasa: Nigdy \nPrzez:{ctx.author}", color = 0xfff904)
        dm.set_author(name=f"Wyciszono cię na serwerze: {ctx.guild}",
                         icon_url=ctx.guild.icon_url)
        dm.set_footer(text=f"Mute id: {ctx.message.id}")

        #add mute role
        await ctx.channel.send(embed=embed)
        await member.send(embed=dm)
        await member.add_roles(role)

    @commands.command(name="unmute")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        data = download_settings(guild_id, "mute")
        role = get(ctx.guild.roles, id=data['role_id'])

        # db connect
        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()

        sql = "SELECT `async_task_id` FROM `mute` WHERE `member_id` = %s AND `gid` = %s"
        val = (member.id, ctx.guild.id)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        print(myresult)
        for a in myresult:
            task_id = a[0]
            task, = [task for task in asyncio.all_tasks() if task.get_name() == task_id]
            task.cancel()
            await self.database_remove(task_id)


        #sprawdzenie czy ma mute
        if role in member.roles:
            await member.remove_roles(role)
            await ctx.channel.send('Pomyślnie usunięto wyciszenie użytkownika!')
        else:
            await ctx.channel.send('Ten użytkownik nie jest wyciszony!')

    @commands.Cog.listener()
    async def on_ready(self):
        await self.recover_system()
#setup
def setup(self):
    print("Moduł cogs.mute załadowany!")