from discord.ext import commands
import mysql.connector
import discord
import settings
from datetime import datetime
import re



class userinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="info")
    async def userinfo(self, ctx, member: discord.Member):
        #dates convertion
        join_time = member.joined_at.strftime("%d/%m/%Y %H:%M:%S")
        create_time = member.created_at.strftime("%d/%m/%Y %H:%M:%S")

        #check voice channel
        if member.voice is None:
            voice = "Brak".upper()
        else:
            voice = f"{member.voice.channel}".upper()

        #top role
        top_role = member.top_role.name
        top_role = re.sub('@', '', top_role, 1)

        #licznik zaproszeń
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter.id == member.id:
                totalInvites += i.uses

        #pseudonim
        if member.display_name is None:
            pseudonim = "Brak"
        else:
            pseudonim = f"{member.display_name}"


        #embed
        embed=discord.Embed(title="Informacje o użytkowniku", color=0xf48afd)
        embed.set_author(name=f"{member}",
                         icon_url=f"{member.avatar_url}")

        embed.add_field(name="📳 Status",
                        value=f"Generalny: {member.status.value} \nPrzegladarka: {member.web_status.value} \nKomputer: {member.desktop_status.value} \nTelefon: {member.mobile_status.value} ",
                        inline=True)
        embed.add_field(name="⌨ Nazwy", value=f"Nick: {member.name} \n Tag: {member.discriminator} \n Pseudonim: {pseudonim} ",
                        inline=True)
        embed.add_field(name="🔈 Aktualny kanał głosowy", value=f"{voice}", inline=True)
        embed.add_field(name="📕 Główna Rola ", value=f"{top_role}", inline=True)
        #embed.add_field(name="📘 Role", value="Admin \n Test \n Test2", inline=True)
        embed.add_field(name="📤 Data dołączenia", value=f"{join_time}", inline=True)
        embed.add_field(name="💌 Ilość zaproszeń", value=f"{totalInvites}", inline=True)
        embed.add_field(name="📅 Data utworzenia konta", value=f"{create_time}", inline=True)
        embed.add_field(name="📟 Id użytkownika", value=f"{member.id}", inline=True)
        embed.add_field(name="🔐 Id uprawnień", value=f"{member.guild_permissions.value}", inline=True)
        embed.set_footer(text=f"Wygenerowano przez: {ctx.author} • {ctx.author.id}")
        embed.set_footer(text=f"Wygenerowano przez: {ctx.author} • {ctx.author.id}")
        await ctx.channel.send(embed=embed)
    #todo: no member tag error
