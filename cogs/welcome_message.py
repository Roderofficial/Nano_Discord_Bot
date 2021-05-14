import discord
from discord.ext import commands

from addons.setting_download import download_settings


class welcome_message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        data = download_settings(member.guild.id, "welcome_message")
        if data['enable'] == 1:
            message = str(data['message'])
            member_full_name = str(member.name) + "#" + str(member.discriminator)
            message = message.replace('$nick$', member.name)
            message = message.replace('$member$', member_full_name)
            message = message.replace('$mention$', member.mention)

            #hex color
            sixteenIntegerHex = int(data['color'].replace("#", ""), 16)
            readableHex = int(hex(sixteenIntegerHex), 0)

            channel = self.bot.get_channel(data['channel_id'])
            embed = discord.Embed(description=message, color=readableHex)
            await channel.send(embed=embed)

            print(data)
            print(message)







# setup
def setup(self):
    print("Moduł cogs.mute załadowany!")
