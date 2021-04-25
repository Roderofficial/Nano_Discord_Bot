from discord.ext import commands
import discord
import settings
import mysql.connector
import random, string
from datetime import datetime
from addons.setting_download import download_settings


class ban_c(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


    def member_banlist_add(self, cog, guild_id, member_id, reason):
        guild_id = str(guild_id)
        member_id = str(member_id)
        reason = str(reason)
        link = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(60))
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
        return f"http://localhost/ban_appeal/{link}"



    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, message, member: discord.Member, *reason):
        reason = " ".join(reason[:])

        #download settings
        settings_data = download_settings(message.guild.id,"ban")
        if settings_data['enable'] == 1:
            #add ban to database
            link = self.member_banlist_add(self, message.guild.id, member.id, reason)

            # generowanie czasu
            kto_zbanowal = str(message.author.display_name) + str('#') + str(message.author.discriminator)
            zbanowany = str(member.display_name) + str('#') + str(member.discriminator)

            #print(zbanowany)
            #print(reason)
            #print(kto_zbanowal)
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
            if settings_data['private_message'] == 1:
                embed = discord.Embed(title="Zostałeś zbanowany na serwerze: " + str(member.guild.name),
                                      description="Przez: " + kto_zbanowal + " \nPowód: **" + str(reason) + "**",
                                      color=0xff0000)
                if settings_data['ban_appeal'] == 1:
                    embed.add_field(name="Odwołaj się od bana", value=f"[Kliknij Tutaj]({link})", inline=False)
                embed.set_thumbnail(url=member.guild.icon_url)
                await member.send(embed=embed)

            # ban
            await member.ban(reason=reason)

    @commands.Cog.listener()
    async def on_member_ban(self,guild,member):
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        settings_data = download_settings(guild.id, "ban")
        channel = guild.get_channel(830370410225729566)
        logs = logs[0]
        if logs.target == member:
            try:
                if settings_data['private_message'] == 1:
                    # private embed
                    embed = discord.Embed(title=f"Zostałeś zbanowany na serwerze: {guild.name}",
                                          description=f"Przez: {logs.user} \nPowód: ** {logs.reason}**",
                                          color=0xff0000)
                    embed.set_thumbnail(url=guild.icon_url)
                    await member.send(embed=embed)
            except Exception:
                pass

    @commands.Cog.listener()
    async def on_member_unban(self,guild,member):
        #print("User unban")
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

    #TODO: COMMAND UNBAN
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

# setup
def setup(self):
    print("Moduł cogs.ban załadowany!")
