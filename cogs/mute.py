from discord.ext import commands
import discord
import settings
import mysql.connector

class mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def create_or_update_database(self, bot, guild_id, role_id):
        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()
        sql = "SELECT data FROM mute_ranks WHERE guild_id = %s"
        await mycursor.execute(sql, (guild_id,))
        myresult = mycursor.fetchone()
        print(myresult)

    async def create_rank_mute(self,*, message):
        print("test")
        guild = message.guild
        print(guild.id)
        # muted_role = await guild.create_role(name="Muted")
        muted_role = 123465
        await self.create_or_update_database(self,str(guild.id),muted_role)
        #muted_role = await guild.create_role(name="Muted")

        await message.channel.send( "Test")


    @commands.command(name="mute")
    @commands.is_owner()
    async def mute(self, message, member: discord.Member, *reason):
        if reason:
            reason = " ".join(reason[:])
        else:
            reason = "Brak."
        print(reason)

        await self.create_rank_mute(self,message.guild.id)
        await message.channel.send("Member: " + str(member.display_name) + " Reason : " + str(reason))

#setup
def setup(self):
    print("Moduł cogs.mute załadowany!")