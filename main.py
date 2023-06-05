from addons.bot_settings import *
from addons.permissions import *
from addons.raports import *
from cogs.acc import *
from cogs.admin import *
from cogs.bad_words_filter import bad_words
from cogs.ban import ban_c
from cogs.kick import *
from cogs.licence import *
from cogs.mini_functions import clear
from cogs.mute import *
from cogs.prefix import *
from cogs.stats import *
from cogs.user_info import *
from cogs.welcome_message import welcome_message
from logs.addlog import messagelog
from logs.voice_channel import voice_channel_logs

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix = get_prefix, intents=intents)
bot.add_cog(messagelog(bot))
bot.add_cog(bad_words(bot))
bot.add_cog(voice_channel_logs(bot))
bot.add_cog(clear(bot))
bot.add_cog(admin(bot))
bot.add_cog(mute(bot))
bot.add_cog(kick_c(bot))
bot.add_cog(ban_c(bot))
bot.add_cog(welcome_message(bot))
bot.add_cog(settings_configuration(bot))
bot.add_cog(licence(bot))
bot.add_cog(userinfo(bot))
bot.add_cog(prefix(bot))
bot.add_cog(stats(bot))
bot.add_cog(acc(bot))
bot.add_cog(permissions(bot))
bot.add_cog(raport(bot))
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="WERSJA 0.1.4 ALFA"))
    print("Bot is ready!")

bot.run('TOKEN HERE')
