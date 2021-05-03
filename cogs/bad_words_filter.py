from discord.ext import commands
import discord
import settings
import mysql.connector


# TODO: FIX FIND WORDS IN STRING

class bad_words(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message(self, message):
        if not message.author.bot:
            if not message.author.guild_permissions.manage_messages:
                if message.content:
                    # select do bazy
                    mydb = mysql.connector.connect(
                        host=settings.db_adres,
                        user=settings.db_login,
                        password=settings.db_password,
                        database=settings.db_base
                    )
                    mycursor = mydb.cursor()
                    sql = "SELECT content FROM bad_words WHERE dc_guild_id = %s"
                    mycursor.execute(sql, (message.guild.id,))
                    myresult = mycursor.fetchall()
                    # print(myresult)
                    filtr_arr = []
                    for a in myresult:
                        filtr_arr.append(a[0])

                    # message content filter
                    for x in filtr_arr:
                        if x.lower() in message.content.lower():
                            await message.delete()
                            # embed send
                            embed = discord.Embed(color=0xff0000)
                            embed.add_field(name="Ostrzeżenie",
                                            value=str(message.author) + " twoja wypowiedź zawiera zakazane frazy.",
                                            inline=False)
                            await message.channel.send(embed=embed, delete_after=10.0)
                            return 0

    @commands.Command
    async def rw(self, message, word):
        print(add_bad_world(int(message.guild.id), word))


def check_word_in_database(gid, word):
    """
    :param gid: Discord guild id
    :param word: Word to check
    :return: True or False
    """
    # select do bazy
    mydb = mysql.connector.connect(
        host=settings.db_adres,
        user=settings.db_login,
        password=settings.db_password,
        database=settings.db_base
    )
    mycursor = mydb.cursor()
    sql = "SELECT content FROM bad_words WHERE dc_guild_id = %s AND content=%s"
    mycursor.execute(sql, (gid, word))
    myresult = mycursor.fetchone()
    print('-FILTR TEST-')
    if myresult is not None:
        print('istnieje w bazie')
        return True
    else:
        print('nie istnieje w bazie')
        return False


def remove_bad_world(gid, word):
    """
    :param gid: Discord Guild id
    :param word: Word
    :return: True or False
    """
    check = check_word_in_database(gid, word)
    if check:
        # select do bazy
        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()
        sql = "DELETE FROM bad_words WHERE dc_guild_id = %s AND content = %s ;"
        mycursor.execute(sql, (gid, word))
        mydb.commit()
        return True
    else:
        return False
def add_bad_world(gid, word):
    """
    :param gid: Discord guild id
    :param word: Word
    :return: True or False
    """
    check = check_word_in_database(gid, word)
    if not check:
        print('Nie ma w bazie')

        return True
    else:
        return False
