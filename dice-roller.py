# bot.py
import os
import random

import discord
import random
import dotenv
from dotenv import load_dotenv
from discord.ext import commands

#getting enviormental variables
#token stored this way for security
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


description = '''This is a test bot'''

#intenets are new, added in 09/01/22, it was the reason my bot could not
#send messages for a long time
intents = discord.Intents.default()
intents.members = True 
intents.messages = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='roll')
async def ping(ctx, sides: int, times: int):
    #ctx refers to the context for the channel where the command was sent from
    sum = 0
    for i in range(0, times):
        sum += random.randint(1,sides)
    await ctx.send(sum)

bot.run(TOKEN)

