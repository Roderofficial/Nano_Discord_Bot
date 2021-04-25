from discord.ext import commands
import discord
import settings
import mysql.connector
from datetime import datetime
from addons.setting_download import *
import re


class settings_configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # main settings
    @commands.group(aliases=['s'])
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        if ctx.invoked_subcommand != None:
            return
        print("main command")


    @settings.command(aliases=['wm'])
    async def welcome_message(self, ctx, variable = None, *value):
        #print("subcommand")
        #print(variable)
        #print(value)
        # enable value
        if variable == "enable":
            value = int(value[0])
            if value == 0 or value == 1:
                #print("Wartość okej")
                update_settings(ctx.guild.id, "welcome_message", variable, value)
                await self.successful_embed(ctx, f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
            else:
                print("Zła wartość")
                print(value)

        # message
        elif variable == "message":
            if value != None:
                value = " ".join(value[:])
                update_settings(ctx.guild.id, "welcome_message", variable, value)
                await self.successful_embed(ctx, f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")

        # color
        elif variable == "color":
            value = value[0]
            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
            print(value)
            if match:
                value = str(value)
                print(value)
                update_settings(ctx.guild.id, "welcome_message", variable, value)
                await self.successful_embed(ctx,f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
        # channel
        elif variable == "channel_id":
            #pobranie zmiennych
            value = value[0]
            channel_id = re.search(r'\d+', value).group()
            #print(channel_id)

            #utworzenie listy kanałów na serwerze
            text_channel_list = []
            for channel in ctx.guild.channels:
                if channel.type[0] == 'text':
                    text_channel_list.append(str(channel.id))
            #print(text_channel_list)

            #Sprawdzenie czy podany kanał istnieje na tym serwerze
            if channel_id in text_channel_list:
                update_settings(ctx.guild.id, "welcome_message", variable, int(channel_id))
                await self.successful_embed(ctx, f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
            else:
                await self.error_embed(ctx, f"**Podany kanał nie znajduje się na tym serwerze.**")


        elif variable == None:
            #embed information for none
            embed = discord.Embed(title="Ustawienia modułu: welcome_messages", description="Alias (dla zaawansowanych): ||**>s wm**||", color=0x00b3ff)
            embed.add_field(name="Włącz/Wyłącz", value=">settings welcome_message 1/0", inline=False)
            embed.add_field(name="Treść powitania",
                            value=">settings welcome_message message Witaj na serwerze $mention$ ```Dozwolone znaczniki: \n$mention$ - oznacza użytkownika (ping) \n$member$ - wypisuje nick użytkownika z tagiem (Nano#1234) \n$nick$ - Wypisuje sam nick użytkownika (Nano)```",
                            inline=False)
            embed.add_field(name="Kolor powiadomienia",
                            value=">settings welcome_message color *#ff9900* \n ```Bot przyjmuje tylko pełny kolor w HEX```",
                            inline=False)
            embed.add_field(name="Kanał powiadomień", value="settings welcome_message channel_id #powitania ```Można podać ID kanału jak również go oznaczyć```",
                            inline=False)
            await ctx.send(embed=embed)

    #not permissions error
    @settings.error
    async def settings_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await self.error_embed(ctx, "**Nie masz odpowiednich uprawnień \n ```Wymagane: Administrator```**")

    # embeds
    async def successful_embed(self, ctx, embed_message):
        embed = discord.Embed(color=0x37ff00)
        embed.add_field(name="👍🏻 Sukces!", value=f"{embed_message}", inline=False)
        await ctx.channel.send(embed=embed)

    #error embed
    async def error_embed(self, ctx, embed_message):
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="❌ Błąd!", value=f"{embed_message}", inline=False)
        await ctx.channel.send(embed=embed)

# setup
def setup(self):
    print("Moduł cogs.mini_functions załadowany!")
