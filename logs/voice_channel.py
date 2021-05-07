from discord.ext import commands
import mysql.connector
import discord
import settings
from datetime import datetime
from addons.setting_download import download_settings
#todo: fix permissions for checking channel

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
    mycursor.close()
    mydb.close()


class voice_channel_logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            database_config = download_settings(str(member.guild.id), "jl_logs")
            #pobranie czasu
            now = datetime.now()
            czas = now.strftime("%d/%m/%Y %H:%M:%S")
            #debug
            """print("----------MEMBER---------")
            print(member)
            print("--------BEFORE---------")
            print(before)
            print("--------AFTER--------")
            print(after)
            print('GID: ' + str(member.guild.id))
            print(database_config['enable'] == 1)
            print(database_config['leave_message'] == 1)
            print(database_config['enable'])
            print(database_config['leave_message'])"""
            #leave channel
            if (not (before.channel is None and after.channel is not None)) and (before.channel != after.channel):
                print("LEAVE")
                if database_config['enable'] == 1 and database_config['leave_message'] == 1:
                    embed = discord.Embed(color=0xc20000)
                    embed.set_author(name=str(member).upper(), icon_url=member.avatar_url)
                    embed.add_field(name="Opuścił/a kanał", value="> " + str(before.channel.name).upper() , inline=True)
                    embed.set_footer(text="Czas: "+ str(czas) + "\nUser id: " + str(member.id))
                    channel = self.bot.get_channel(database_config['channel_id'])
                    await channel.send(embed=embed)
                # database insert
                db_insert(0, member.guild.id, before.channel.id, member.id)


            #join channel
            if ((before.channel is None and after.channel is not None) or (before.channel is not None and after.channel is not None)) and (before.channel != after.channel):
                print("JOIN")
                #embed join
                if database_config['enable'] == 1 and database_config['join_message'] == 1:
                    embed = discord.Embed(color=0x00d607)
                    embed.set_author(name=str(member).upper(), icon_url=member.avatar_url)
                    embed.add_field(name="Dołączył/a na kanał", value="> " + str(after.channel.name).upper() , inline=True)
                    embed.set_footer(text="Czas: "+ str(czas) + "\nUser id: " + str(member.id))
                    channel = self.bot.get_channel(database_config['channel_id'])
                    await channel.send(embed=embed)
                # database insert
                db_insert(1,member.guild.id,after.channel.id,member.id)
        except:
            pass
