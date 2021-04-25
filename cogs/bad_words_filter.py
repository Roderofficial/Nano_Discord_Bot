from discord.ext import commands
import discord
import settings
import mysql.connector
#TODO: FIX FIND WORDS IN STRING

class bad_words(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.content:
                #select do bazy
                mydb = mysql.connector.connect(
                    host=settings.db_adres,
                    user=settings.db_login,
                    password=settings.db_password,
                    database=settings.db_base
                )
                mycursor = mydb.cursor()
                sql = "SELECT content FROM bad_words WHERE dc_guild_id = %s"
                mycursor.execute(sql,(message.guild.id, ))
                myresult = mycursor.fetchall()
                print(myresult)
                filtr_arr = []
                for a in myresult:
                    filtr_arr.append(a[0])

                #message content filter
                for x in filtr_arr:
                    if x in message.content:
                        await message.delete()
                        #embed send
                        embed = discord.Embed(color=0xff0000)
                        embed.add_field(name="Ostrzeżenie", value= str(message.author) + " twoja wypowiedź zawiera zakazane frazy.", inline=False)
                        await message.channel.send(embed=embed)
                        return 0
