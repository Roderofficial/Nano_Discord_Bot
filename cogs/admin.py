from discord.ext import commands
import discord
import settings
import mysql.connector

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None



    @commands.command(hidden=True)
    @commands.is_owner()
    async def logout(self, message):
        await message.channel.send("``` Wyłączanie... ```")
        await self.bot.logout()


    #check cog
    @commands.command(hidden=True)
    @commands.is_owner()
    async def cogcheck(self, message, cog_name):
        try:
            self.bot.load_extension(cog_name)
            await message.channel.send("``` Wtyczka załadowana ```")
        except commands.ExtensionAlreadyLoaded:
            await message.channel.send("``` Wtyczka załadowana ```")
        except commands.ExtensionNotFound:
            await message.channel.send("``` Nie znaleziono wtyczki ```")
        except Exception as e:
            await message.channel.send("```" + str(e) + "```")


    #unload cog
    # TODO: FIX COG UNLOAD
    @commands.command(hidden=True)
    @commands.is_owner()
    async def cogunload(self, message, cog_name):
        try:
            self.bot.unload_extension(cog_name)
            await message.channel.send("```Wtyczka "+ str(cog_name) +" została pomyślnie wyłączona```")
        except Exception as e:
            await message.channel.send("```" + str(e) + "```")



    #reload cogs
    #TODO: FIX COG RELOAD
    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cogreload(self, ctx, *, cog: str):
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


#setup
def setup(self):
    print("Moduł cogs.admin załadowany!")