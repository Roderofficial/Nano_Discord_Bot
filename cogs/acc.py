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


    async def used_channels_in_category(self, cid):
        category_channel = self.bot.get_channel(cid)
        print(category_channel)
        count = 0
        for a in category_channel.channels:
            if a.type.name == 'voice':
                if len(a.members) > 0:
                    count = count + 1
        return count

    async def free_channel_in_category(self, cid):
        category_channel = self.bot.get_channel(cid)
        count = 0
        for a in category_channel.channels:
            if a.type.name == 'voice':
                if len(a.members) == 0:
                    count = count + 1
        print(count)
        return count

    async def get_config(self, cid):
        # select do bazy
        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM auto_channels WHERE category_id = %s"
        mycursor.execute(sql, (str(cid),))
        myresult = mycursor.fetchone()
        print(myresult)
        return myresult

    async def update_status(self, cid):
        category_bot = self.bot.get_channel(cid)
        guild = category_bot.guild
        print('Update channel')
        settings = await self.get_config(cid)

        used = await self.used_channels_in_category(cid)
        free = await self.free_channel_in_category(cid)
        free = int(free)
        used = int(used)
        total = free + used
        channel_number = total

        #debug
        print(f"Used: {used}")
        print(f"Total: {total}")
        print(f"Settings min: {settings[4]}")


        #dodawanie kanałów w przypadku za małej ilości minimalnej
        print('Check if')
        if settings[4] > total:
            print("IF OK")

            for a in range(total+1, settings[4]+1):
                channel_number = channel_number + 1
                title = settings[6].decode("utf-8")
                title = str(title)
                title = title.replace('$number$', str(channel_number))
                print(title)
                channel = await guild.create_voice_channel(str(title), category=category_bot)


        #dodanie kanałów w przypadku ilości zamałej po zajętych
        free = await self.free_channel_in_category(cid)
        free = int(free)
        if settings[5] >= free:
            print("Free IF OK")
            for a in range(free + 1, settings[5] + 1):
                channel_number = channel_number + 1
                title = settings[6].decode("utf-8")
                title = str(title)
                title = title.replace('$number$', str(channel_number))
                print(title)
                channel = await guild.create_voice_channel(str(title), category=category_bot)

        #usunięcie pustych kanałów bez użytkowników

        #usunięcie kanałów jeśli za dużo wolnych








    @commands.command()
    async def tc(self,ctx):
        await self.update_status(840115485341384744)
