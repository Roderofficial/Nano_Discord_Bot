from discord.ext import commands
import mysql.connector
import discord
import settings
from datetime import datetime


# database insert
def db_insert(action, dc_guild_id, dc_voice_channel_id, dc_client_id):
    # database insert
    mydb = mysql.connector.connect(
        host=settings.db_adres,
        user=settings.db_login,
        password=settings.db_password,
        database=settings.db_base
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO `jl_logs` (`action`, `dc_guild_id`, `dc_voice_channel_id`, `dc_client_id`) VALUES ('%s', '%s', '%s', '%s')"
    val = (action, dc_guild_id, dc_voice_channel_id, dc_client_id)
    mycursor.execute(sql, val)
    mydb.commit()


class voice_channel_logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #pobranie czasu
        now = datetime.now()
        czas = now.strftime("%d/%m/%Y %H:%M:%S")
        print("----------MEMBER---------")
        print(member)
        print("--------BEFORE---------")
        print(before)
        print("--------AFTER--------")
        print(after)
        print('GID: ' + str(member.guild.id))
        #join channel
        if before.channel is None and after.channel is not None:
            print("JOIN")
            #database insert
            #db_insert(1,)
            #embed join
            embed = discord.Embed(color=0x00d607)
            embed.set_author(name=member, icon_url=member.avatar_url)
            embed.add_field(name="Dołączył/a na kanał", value=after.channel.name , inline=True)
            embed.set_footer(text="Czas: "+ str(czas) + "\nUser id: " + str(member.id))
            channel = self.bot.get_channel(737070027424923670)
            await channel.send(embed=embed)
            db_insert(1,member.guild.id,after.channel.id,member.id)

        #leave channel
        if not (before.channel is None and after.channel is not None):
            print("LEAVE")
            embed = discord.Embed(color=0xe60000)
            embed.set_thumbnail(url="https://cdn.icon-icons.com/icons2/2108/PNG/512/discord_icon_130958.png")
            embed.add_field(name=str(member), value="Opuścił/a kanał \n" + before.channel.name , inline=True)
            embed.set_footer(text=czas)
            channel = self.bot.get_channel(737070027424923670)
            await channel.send(embed=embed)
            db_insert(0, member.guild.id, before.channel.id, member.id)