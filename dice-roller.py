# bot.py
import os
import random

import discord
import random
import dotenv
from dotenv import load_dotenv
from discord.ext import commands
from discord import embeds
from character import character

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

#events 
@bot.event
async def on_connect():
    print(f'{bot.user} has connected to Discord!')
@bot.event 
async def on_disconnect():
    print(f'{bot.user} has disconnected from Discord!')

#commands
@bot.command(name='roll')
async def roll(ctx, sides: int, times: int):
    #ctx refers to the context for the channel where the command was sent from
    sum = 0
    for i in range(0, times):
        sum += random.randint(1,sides)
    await ctx.send(sum)

@bot.command(name = "showchar")
async def showchar(ctx):
    #will print out the character information as an embed 
    chara = character("Chiko")
    embed = discord.Embed(title= f'{chara.name}', description="You have a character")
    fields = [("Str", f'{chara.str}', True),
              ("Dex", f'{chara.dex}', True),
              ("Con", f'{chara.con}', True),
              ("Int", f'{chara.intel}', True),
              ("Wis", f'{chara.wis}', True),
              ("Cha", f'{chara.cha}', True)]
    for name, value, inline in fields: 
        embed.add_field(name = name, value = value, inline=inline)
    await ctx.send(embed=embed)

bot.run(TOKEN)

