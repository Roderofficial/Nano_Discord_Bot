from discord.ext import commands
import discord
import settings
import mysql.connector
from datetime import datetime
from addons.setting_download import *


class kick_c(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, message, member: discord.Member, *reason):
        #download settings
        settings_data = download_settings(message.guild.id,"kick")

        #try check if enable
        try:
            if settings_data['enable'] == 1:
                reason = " ".join(reason[:])

                # generowanie czasu
                kto_zbanowal = str(message.author.display_name) + str('#') + str(message.author.discriminator)
                zbanowany = str(member.display_name) + str('#') + str(member.discriminator)
                print(zbanowany)
                print(reason)
                print(kto_zbanowal)
                # pobranie czasu
                now = datetime.now()
                czas = now.strftime("%d/%m/%Y %H:%M:%S")

                # kick embed on server
                embed = discord.Embed(title="Użytkownik " + zbanowany + " został wyrzucony",
                                      description="Przez: " + kto_zbanowal + " \nPowód: **" + str(reason) + "**",
                                      color=0xff0000)
                embed.set_footer(text="Czas: " + czas + "\nClient id:" + str(member.id))
                embed.set_thumbnail(url=member.avatar_url)
                await message.channel.send(embed=embed)

                # private embed
                try:
                    if settings_data['private_message'] == 1:
                        embed = discord.Embed(title="Zostałeś wyrzucony z serwera: " + str(member.guild.name),
                                              description="Przez: " + kto_zbanowal + " \nPowód: **" + str(reason) + "**",
                                              color=0xff0000)
                        embed.set_thumbnail(url=member.guild.icon_url)
                        await member.send(embed=embed)
                except Exception:
                    None

                # kick
                await member.kick(reason=reason)
        except Exception as e:
            print(f"Enable kick e: {e}")
            pass
# setup
def setup(self):
    print("Moduł cogs.mute załadowany!")
