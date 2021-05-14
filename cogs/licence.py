import discord
import mysql.connector
from discord.ext import commands

import settings


class licence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_ready(self):
        print('- Sprawdzanie licencji -')
        for guild in self.bot.guilds:
            print(guild.id)

    @commands.command(name="licencja")
    async def moja_licencja(self,ctx):
        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM licences WHERE guild_id = %s"
        mycursor.execute(sql, (ctx.guild.id,))
        myresult = mycursor.fetchone()
        mycursor.close()
        mydb.close()
        #print(myresult)
        if myresult is None:
            await self.licence_embed(ctx, ctx.guild.name)
        else:
            color = 0xeeff00
            await self.licence_embed(ctx,ctx.guild.name,myresult[2].decode(), "Premium", myresult[3], myresult[0], color)


    async def licence_embed(self,ctx, guild_name, author="System",licence_type="Free", expire_time="Nigdy", id=None, color=None):
        if color is None:
            embed = discord.Embed()
        else:
            embed = discord.Embed(color=color)
        embed.add_field(name=f"🔑 Licencja dla serwera: {guild_name}",
                        value=f"\n✍🏻 Wydana przez: **{author}** \n\n📑 Typ licencji: **{licence_type}** \n\n🕘 Wygasa: **{expire_time}**", inline=False)
        if id is not None:
            embed.set_footer(text=f"Id licencji: {id}")
        await ctx.channel.send(embed=embed)

def premium_licence_check(gid):
    mydb = mysql.connector.connect(
        host=settings.db_adres,
        user=settings.db_login,
        password=settings.db_password,
        database=settings.db_base
    )
    mycursor = mydb.cursor()
    sql = "SELECT * FROM licences WHERE guild_id = %s"
    mycursor.execute(sql, (gid,))
    myresult = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    # print(myresult)
    if myresult is None:
        return False
    else:
        return True

# setup
def setup(self):
    print("Moduł cogs.mute załadowany!")
