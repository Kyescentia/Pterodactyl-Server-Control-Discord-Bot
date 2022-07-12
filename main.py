import discord
from discord.ext import commands
from utils.config import token

bot = commands.Bot(command_prefix="?")

@bot.event
async def on_ready():
    print(f'bot online')

bot.load_extension('cogs.petro')
                                 
bot.run(token)