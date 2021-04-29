from discord.ext import commands
import mysql.connector
import discord
import settings

class messagelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self,message):
        if not message.author.bot:
            #check empty
            if not message.content: return 0
            #await message.channel.send('<3')
            #await message.channel.send("GID: " + str(message.guild.id) + " CID: " + str(message.channel.id) + " CLIID: " + str(message.author.id) + " MID: " + str(message.id) + " M: " + str(message.content))
            #database insert
            mydb = mysql.connector.connect(
                host=settings.db_adres,
                user=settings.db_login,
                password=settings.db_password,
                database=settings.db_base
            )
            mycursor = mydb.cursor()

            sql = "INSERT INTO `messages_logs` (`dc_guild_id`, `dc_channel_id`, `dc_client_id`, `dc_message_id`, `message`) VALUES (%s, %s, %s, %s, %s)"
            val = (message.guild.id, message.channel.id, message.author.id, message.id, message.content)
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()