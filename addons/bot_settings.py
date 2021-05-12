import re

import discord
from discord.ext import commands

from addons.setting_download import *
from cogs.ban import member_banlist_check
from cogs.licence import premium_licence_check
from cogs.prefix import get_prefix
from cogs.bad_words_filter import get_bad_words_list_string,check_word_in_database,add_bad_world,remove_bad_world

class settings_configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # main settings
    @commands.group(name="settings",aliases=['s'])
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        print("main command")

    """
    ############################
    ###    WELCOME_MESSAGE   ###
    ############################
    """

    @settings.command(aliases=['wm'])
    async def welcome_message(self, ctx, variable=None, *value):
        # print("subcommand")
        # print(variable)
        # print(value)
        # enable value
        if variable == "enable":
            value = int(value[0])
            if value == 0 or value == 1:
                # print("Wartość okej")
                update_settings(ctx.guild.id, "welcome_message", variable, value)
                await self.successful_embed(ctx, f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
            else:
                await self.error_embed(ctx)

        # message
        elif variable == "message":
            if value != None:
                value = " ".join(value[:])
                update_settings(ctx.guild.id, "welcome_message", variable, value)
                await self.successful_embed(ctx, f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
            else:
                await self.error_embed(ctx)

        # color
        elif variable == "color":
            value = value[0]
            match = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
            print(value)
            if match:
                value = str(value)
                print(value)
                update_settings(ctx.guild.id, "welcome_message", variable, value)
                await self.successful_embed(ctx, f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
            else:
                await self.error_embed(ctx)
        # channel
        elif variable == "channel_id":
            # pobranie zmiennych
            value = value[0]
            try:
                channel_id = re.search(r'\d+', value).group()
            except:
                await self.error_embed(ctx)
                return 0
            # print(channel_id)

            # utworzenie listy kanałów na serwerze
            text_channel_list = []
            for channel in ctx.guild.channels:
                if channel.type[0] == 'text':
                    text_channel_list.append(str(channel.id))
            # print(text_channel_list)

            # Sprawdzenie czy podany kanał istnieje na tym serwerze
            if channel_id in text_channel_list:
                update_settings(ctx.guild.id, "welcome_message", variable, int(channel_id))
                await self.successful_embed(ctx, f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
            else:
                await self.error_embed(ctx, f"**Podany kanał nie znajduje się na tym serwerze.**")


        elif variable is None:
            # embed information for none
            embed = discord.Embed(title="Ustawienia modułu: welcome_messages",
                                  description="Alias (dla zaawansowanych): ||**>s wm**||", color=0x00b3ff)
            embed.add_field(name="Włącz/Wyłącz", value=f"{get_prefix(self,ctx)}settings welcome_message 1/0", inline=False)
            embed.add_field(name="Treść powitania",
                            value=f"{get_prefix(self,ctx)}settings welcome_message message Witaj na serwerze $mention$ ```Dozwolone znaczniki: \n$mention$ - oznacza użytkownika (ping) \n$member$ - wypisuje nick użytkownika z tagiem (Nano#1234) \n$nick$ - Wypisuje sam nick użytkownika (Nano)```",
                            inline=False)
            embed.add_field(name="Kolor powiadomienia",
                            value=f"{get_prefix(self,ctx)}settings welcome_message color *#ff9900* \n ```Bot przyjmuje tylko pełny kolor w HEX```",
                            inline=False)
            embed.add_field(name="Kanał powiadomień",
                            value=f"{get_prefix(self,ctx)}settings welcome_message channel_id #powitania ```Można podać ID kanału jak również go oznaczyć```",
                            inline=False)
            await ctx.send(embed=embed)
        else:
            await self.error_embed(ctx, "Podane polecenie nie istnieje")

    """
    #################
    ###    KICK   ###
    #################
    """

    @settings.command(name="kick")
    async def kick(self, ctx, variable=None, *value):
        print("Kick edit")
        # todo: kick settings
        # enable kick
        if variable == "enable":
            try:
                value = int(value[0])
                if value == 0 or value == 1:
                    update_settings(ctx.guild.id, "kick", variable, value)
                    await self.successful_embed(ctx,
                                                f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                else:
                    await self.error_embed(ctx)
            except:
                print(f"Error:")
                await self.error_embed(ctx)
                pass

        # private message
        elif variable == "private_message":
            try:
                value = int(value[0])
                if value == 0 or value == 1:
                    update_settings(ctx.guild.id, "kick", variable, value)
                    await self.successful_embed(ctx,
                                                f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                else:
                    await self.error_embed(ctx)
            except Exception:
                await self.error_embed(ctx)



        # send info
        elif variable == None:
            embed = discord.Embed(title="Ustawienia modułu: kick", description="Alias dla zaawansowanych: ||>s kick||",
                                  color=0x00b3ff)
            embed.add_field(name="Włącz/Wyłącz", value=f"{get_prefix(self,ctx)}settings kick enable 0/1", inline=False)
            embed.add_field(name="Prywatna wiadomość do użytkownika po wyrzuceniu",
                            value=f"{get_prefix(self,ctx)}settings kick private_message 0/1", inline=True)
            embed.set_footer(text="Ten moduł korzysta z uprawnień Discord. Uprawnienie: kick")
            await ctx.channel.send(embed=embed)
        else:
            await self.error_embed(ctx, "Podane polecenie nie istnieje")

    """
    #################
    ###    BAN    ###
    #################
    """

    @settings.command(name="ban")
    async def ban(self, ctx, variable=None, *value):
        print("ban edit")
        # todo: kick settings
        # enable kick
        if variable == "enable":
            try:
                value = int(value[0])
                if value == 0 or value == 1:
                    update_settings(ctx.guild.id, "ban", variable, value)
                    await self.successful_embed(ctx,
                                                f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                else:
                    await self.error_embed(ctx)
            except:
                print(f"Error:")
                await self.error_embed(ctx)
                pass

        # private message
        elif variable == "private_message":
            try:
                value = int(value[0])
                if value == 0 or value == 1:
                    update_settings(ctx.guild.id, "ban", variable, value)
                    await self.successful_embed(ctx,
                                                f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                else:
                    await self.error_embed(ctx)
            except Exception:
                await self.error_embed(ctx)

        # ban appeal
        elif variable == "ban_appeal":
            if(premium_licence_check(ctx.guild.id)):
                try:
                    value = int(value[0])
                    if value == 0 or value == 1:
                        update_settings(ctx.guild.id, "ban", variable, value)
                        await self.successful_embed(ctx,
                                                    f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                    else:
                        await self.error_embed(ctx)
                except Exception:
                    await self.error_embed(ctx)
            else:
                await self.error_embed(ctx,"Funkcja, którą próbujesz konfigurować jest jedynie dla wersji **premium**")





        # send info
        elif variable == None:
            embed = discord.Embed(title="Ustawienia modułu: ban", description="Alias dla zaawansowanych: ||>s ban||",
                                  color=0x00b3ff)
            embed.add_field(name="Włącz/Wyłącz", value=f"{get_prefix(self,ctx)}settings ban enable 0/1", inline=False)
            embed.add_field(name="Prywatna wiadomość do użytkownika po wyrzuceniu",
                            value=f"{get_prefix(self,ctx)}settings ban private_message 0/1", inline=True)
            embed.add_field(name="★ Apelacje od bana Włączone/Wyłączone", value=f"{get_prefix(self,ctx)}settings ban ban_appeal 0/1",
                            inline=False)
            embed.set_footer(text="Ten moduł korzysta z uprawnień Discord. Uprawnienie: ban")
            await ctx.channel.send(embed=embed)
        else:
            await self.error_embed(ctx, "Podane polecenie nie istnieje")



    #|---------GLOBAL--------|
    @settings.command(name="global")
    async def global_settings(self, ctx, variable=None, *value):
        print("global edit")
        # enable kick
        if variable == "prefix":
            value = value[0]
            try:
                if value is not None:
                    update_settings(ctx.guild.id, "global", variable, value)
                    await self.successful_embed(ctx,
                                                f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                else:
                    await self.error_embed(ctx)
            except:
                print(f"Error:")
                await self.error_embed(ctx)
                pass


        # send info
        elif variable == None:
            embed = discord.Embed(title="Ustawienia modułu: ban", description="Alias dla zaawansowanych: ||>s ban||",
                                  color=0x00b3ff)
            embed.add_field(name="Prefix", value=">settings global prefix >", inline=False)

            await ctx.channel.send(embed=embed)
        else:
            await self.error_embed(ctx, "Podane polecenie nie istnieje")


    #
    # VOICE CHANNEL LOGS
    #
    #settings voice channel logs
    @settings.command(name="jll")
    async def jllogs(self, ctx, variable=None, *value):
        print("jllogs edit")
        # enable voice channel logs
        if variable == "enable":
            try:
                value = int(value[0])
                if value == 0 or value == 1:
                    update_settings(ctx.guild.id, "jl_logs", variable, value)
                    await self.successful_embed(ctx,
                                                f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                else:
                    await self.error_embed(ctx)
            except:
                print(f"Error:")
                await self.error_embed(ctx)
                pass

        # join message
        elif variable == "join_message":
            try:
                value = int(value[0])
                if value == 0 or value == 1:
                    update_settings(ctx.guild.id, "jl_logs", variable, value)
                    await self.successful_embed(ctx,
                                                f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                else:
                    await self.error_embed(ctx)
            except Exception:
                await self.error_embed(ctx)

        # leave message
        elif variable == "leave_message":
            try:
                value = int(value[0])
                if value == 0 or value == 1:
                    update_settings(ctx.guild.id, "jl_logs", variable, value)
                    await self.successful_embed(ctx,
                                                f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
                else:
                    await self.error_embed(ctx)
            except Exception:
                await self.error_embed(ctx)

        #channel id logs
        elif variable == "channel_id":
            # pobranie zmiennych
            value = value[0]
            try:
                channel_id = re.search(r'\d+', value).group()
            except:
                await self.error_embed(ctx)
                return 0
            # print(channel_id)

            # utworzenie listy kanałów na serwerze
            text_channel_list = []
            for channel in ctx.guild.channels:
                if channel.type[0] == 'text':
                    text_channel_list.append(str(channel.id))
            # print(text_channel_list)

            # Sprawdzenie czy podany kanał istnieje na tym serwerze
            if channel_id in text_channel_list:
                update_settings(ctx.guild.id, "jl_logs", variable, int(channel_id))
                await self.successful_embed(ctx, f"Wartość **{variable}** została ustawiona pomyślnie na **{value}**")
            else:
                await self.error_embed(ctx, f"**Podany kanał nie znajduje się na tym serwerze.**")

        # send info
        elif variable == None:
            embed = discord.Embed(title="Ustawienia modułu: ban", description="Alias dla zaawansowanych: ||>s ban||",
                                  color=0x00b3ff)
            embed.add_field(name="Włącz/Wyłącz", value=f"{get_prefix(self,ctx)}settings ban enable 0/1", inline=False)
            embed.add_field(name="Prywatna wiadomość do użytkownika po wyrzuceniu",
                            value=f"{get_prefix(self,ctx)}settings ban private_message 0/1", inline=True)
            embed.add_field(name="★ Apelacje od bana Włączone/Wyłączone", value=f"{get_prefix(self,ctx)}settings ban ban_appeal 0/1",
                            inline=False)
            embed.set_footer(text="Ten moduł korzysta z uprawnień Discord. Uprawnienie: ban")
            await ctx.channel.send(embed=embed)
        else:
            await self.error_embed(ctx, "Podane polecenie nie istnieje")

    @settings.command(name="message_filter", aliases=['mf'])
    async def bw_filter(self, ctx, variable=None, *value):
        print("bw edit")
        # get list of words
        if variable == "list":
            embed = discord.Embed(color=0xe7383d)
            embed.add_field(name="Lista filtrowanych fraz", value=f"```{get_bad_words_list_string(ctx.guild.id)}```", inline=False)
            await ctx.channel.send(embed=embed)


        # add word
        elif variable == "add":
            try:
                value = " ".join(value[:])
                if value is not None:
                    if add_bad_world(ctx.guild.id,value):
                        await self.successful_embed(ctx, f"Pomyślnie dodano frazę: ``{value}``")
                    else:
                        await self.error_embed(ctx, f"Dodanie frazy ``{value}`` zakończyło się niepowodzeniem, być może znajduje się już ona na liście.")

                else:
                    await self.error_embed(ctx)
            except Exception:
                await self.error_embed(ctx)

        # remove word
        elif variable == "remove":
            try:
                value = " ".join(value[:])
                if value is not None:
                    if remove_bad_world(ctx.guild.id,value):
                        await self.successful_embed(ctx, f"Pomyślnie usinięto frazę: ``{value}``")
                    else:
                        await self.error_embed(ctx, f"Nie udało się usunać frazy ``{value}``, być może nie ma jej na liście")


            except Exception:
                await self.error_embed(ctx)

        elif variable == None:
            embed = discord.Embed(title="Ustawienia modułu: message_filter", description="Alias dla zaawansowanych: ||>s mf||",
                                  color=0x00b3ff)
            embed.add_field(name="Lista fraz", value=f"{get_prefix(self,ctx)}settings mf list", inline=False)
            embed.add_field(name="Dodanie frazy do listy",
                            value=f"{get_prefix(self,ctx)}settings mf add text", inline=True)
            embed.add_field(name="Usunięcie frazy z listy", value=f"{get_prefix(self,ctx)}settings mf remove text",
                            inline=False)
            embed.set_footer(text="Ten moduł korzysta z uprawnień Discord. Podczas sprawdzania pomijani są użytkownicy z uprawnieniem: zarządzanie wiadomościami.")
            await ctx.channel.send(embed=embed)
        else:
            await self.error_embed(ctx, "Podane polecenie nie istnieje")
    # not permissions error
    @settings.error
    async def settings_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await self.error_embed(ctx, "**Nie masz odpowiednich uprawnień \n ```Wymagane: Administrator```**")

    # embeds
    async def successful_embed(self, ctx, embed_message):
        """
        :param ctx: CTX
        :param embed_message: Message for embed
        :return: None
        """
        embed = discord.Embed(color=0x37ff00)
        embed.add_field(name="👍🏻 Sukces!", value=f"{embed_message}", inline=False)
        await ctx.channel.send(embed=embed)

    # error embed
    async def error_embed(self, ctx, embed_message="Wartość nie jest poprawna"):
        """
        :param ctx: CTX
        :param embed_message: Message for embed
        :return: None
        """
        embed = discord.Embed(color=0xff0000)
        embed.add_field(name="❌ Błąd!", value=f"{embed_message}", inline=False)
        await ctx.channel.send(embed=embed)



# setup
def setup():
    print("Moduł cogs.mini_functions załadowany!")
