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

# client = discord.Client()

# @client.event
# async def on_ready():
#     print(f'{client.user} has connected to Discord!')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content == 'ping!':
#         await message.channel.send('pong')

description = '''This is a test bot'''

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='ping')
async def ping(ctx):
    #ctx refers to the context for the channel where the command was sent from
    print('pong!')
    response = 'pong!'
    await ctx.send(response)

bot.run(TOKEN)

