import random
import string
from datetime import datetime

import discord
import mysql.connector
from discord.ext import commands

import settings
from addons.setting_download import download_settings


# todo: doubled messages


class ban_c(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    def member_banlist_add(self, cog, guild_id, member_id, reason):
        """
        :param cog: Auto, empty
        :param guild_id: Discord guild id
        :param member_id: Discord member id
        :param reason: Ban reason
        :return: Ban appeal code
        """
        guild_id = str(guild_id)
        member_id = str(member_id)
        reason = str(reason)
        link = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()

        sql = "INSERT INTO `ban_list` (`id`, `dc_guild_id`, `dc_member_id`, `reason`, `link`) VALUES (NULL, %s, %s, %s, %s)"
        val = (guild_id, member_id, reason, link)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()
        return str(link)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, message, member: discord.Member, *reason):
        # reason chceck
        if len(reason[0]) == 0:
            reason = "Brak"
        else:
            reason = " ".join(reason[:])

        # download settings
        settings_data = download_settings(message.guild.id, "ban")
        try:
            if settings_data['enable'] == 1:
                # add ban to database
                link = self.member_banlist_add(self, message.guild.id, member.id, reason)

                # generowanie czasu
                kto_zbanowal = str(message.author.display_name) + str('#') + str(message.author.discriminator)
                zbanowany = str(member.display_name) + str('#') + str(member.discriminator)

                # print(zbanowany)
                # print(reason)
                # print(kto_zbanowal)
                # pobranie czasu
                now = datetime.now()
                czas = now.strftime("%d/%m/%Y %H:%M:%S")

                # ban embed on server
                embed = discord.Embed(title="Użytkownik " + zbanowany + " został zbanowany",
                                      description="Przez: " + kto_zbanowal + " \nPowód: **" + str(reason) + "**",
                                      color=0xff0000)
                embed.set_footer(text="Czas: " + czas + "\nClient id:" + str(member.id))
                embed.set_thumbnail(url=member.avatar_url)
                await message.channel.send(embed=embed)

                # private embed
                try:
                    if settings_data['private_message'] == 1:
                        embed = discord.Embed(title="Zostałeś zbanowany na serwerze: " + str(member.guild.name),
                                              description="Przez: " + kto_zbanowal + " \nPowód: **" + str(
                                                  reason) + "**",
                                              color=0xff0000)
                        try:
                            if settings_data['ban_appeal'] == 1:
                                embed.add_field(name="Odwołaj się od bana", value=f"```>a {link} [Treść twojego odwołania]```", inline=False)
                        except:
                            None
                        embed.set_thumbnail(url=member.guild.icon_url)
                        await member.send(embed=embed)
                except Exception:
                    None

                # ban
                await member.ban(reason=reason)
        except Exception:
            pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        if not member_banlist_check(guild.id, member.id):

            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
            logs = logs[0]
            print(logs.reason)
            link = self.member_banlist_add(self, guild.id, member.id, str(logs.reason))
            settings_data = download_settings(guild.id, "ban")

            if logs.target == member:
                try:
                    if settings_data['private_message'] == 1:
                        # private embed
                        embed = discord.Embed(title=f"Zostałeś zbanowany na serwerze: {guild.name}",
                                              description=f"Przez: {logs.user} \nPowód: ** {logs.reason}**",
                                              color=0xff0000)
                        try:
                            if settings_data['ban_appeal'] == 1:
                                embed.add_field(name="Odwołaj się od bana", value=f"```>a {link} [Treść twojego odwołania]```", inline=False)
                        except:
                            None
                        embed.set_thumbnail(url=guild.icon_url)
                        await member.send(embed=embed)
                except Exception:
                    pass
    """ADNOTACJA:
    Jak pozbyłem się duplikacji wiadomości? Wystarczy, że przed on member ban użytkownik sprawdzi czy już jest ktoś zbanowany, jeśli tak to nie wysyła wiadomości ani nie dodaje
    """
    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        # print("User unban")
        guild_id = int(guild.id)
        member_id = int(member.id)

        mydb = mysql.connector.connect(
            host=settings.db_adres,
            user=settings.db_login,
            password=settings.db_password,
            database=settings.db_base
        )
        mycursor = mydb.cursor()

        sql = "DELETE FROM ban_list WHERE `dc_guild_id` = %s AND `dc_member_id` = %s"
        val = (guild_id, member_id)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        mydb.close()

    """
    #################
    ###    BAN    ###
    #################
    """

    @commands.command(name="a")
    async def ban_appeal(self,ctx):
        print("Appeal")

    # TODO: COMMAND UNBAN
    """
    
    @commands.command
    @commands.has_permissions(ban_members=True)
    async def unabn(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.banned_users

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                """

def member_banlist_check(guild_id, member_id):

    mydb = mysql.connector.connect(
        host=settings.db_adres,
        user=settings.db_login,
        password=settings.db_password,
        database=settings.db_base
    )
    mycursor = mydb.cursor()

    sql = "SELECT * FROM `ban_list` WHERE dc_guild_id = %s AND dc_member_id = %s"
    val = (guild_id, member_id)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    mycursor.close()
    mydb.close()
    if myresult is None:
        return False
    else:
        return True



# setup
def setup():
    print("Moduł cogs.ban załadowany!")
