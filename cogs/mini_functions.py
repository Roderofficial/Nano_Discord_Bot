from datetime import datetime

import discord
from discord.ext import commands


class clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    #clear command
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self,message, amount=5):

        # generowanie czasu
        # pobranie czasu
        now = datetime.now()
        czas = now.strftime("%d/%m/%Y %H:%M:%S")

        #usuwanie
        await message.channel.purge(limit=amount)

        #embed
        embed = discord.Embed(description="Pomyślnie usunięto " + str(amount) + " wiadomości!", color=0x009dff)
        embed.set_footer(text="Czas: " + str(czas))
        await message.channel.send(embed=embed)




#setup
def setup(self):
    print("Moduł cogs.mini_functions załadowany!")
