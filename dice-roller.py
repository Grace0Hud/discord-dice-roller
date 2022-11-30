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
from lib.db import db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
#getting enviormental variables
#token stored this way for security
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
description = '''This is a test bot'''
scheduler = AsyncIOScheduler()
db.autosave(scheduler)
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
@bot.event 
async def on_ready():
    scheduler.start()
    print(f'{bot.user} is ready!')

#commands
@bot.command(name='roll')
async def roll(ctx, sides: int, times: int):
    #ctx refers to the context for the channel where the command was sent from
    sum = 0
    for i in range(0, times):
        sum += random.randint(1,sides)
    await ctx.send(sum)

@bot.command(name = 'showchar')
async def showchar(ctx, charaName = " "):
    #will print out the character information as an embed 
    userID = ctx.author.id
    if(db.record('SELECT ChaName FROM characterLists WHERE UserID = ?', userID) is None):
        await ctx.send("You do not have any characters to show.\n To create one, type \'!newcha [character name]\'")
    elif(db.record('SELECT ChaName FROM characterLists WHERE UserID = ? AND ChaName =?', userID, charaName) is None):
        await ctx.send("You don't have a character by that name")
    else:
        chara = character.process(userID, charaName)
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

@bot.command(name = 'newcha')
async def newcha(ctx, chaName: str):
    userID = ctx.author.id
    #checks to see if there is already a character created for the individual
    #if there isn't, creates the character, if there is it warns them they 
    #already have one
    if(chaName is None):
        await ctx.send('Command: !newcha [characterName]')
    elif(db.record('SELECT chaName FROM characterLists WHERE UserID = ? AND chaName = ?', userID, chaName) is not None):
        await ctx.send('You already have a character by that name.')
    else:
        db.execute('INSERT INTO characterLists (UserID, ChaName) VALUES (?,?)', userID, chaName)
        await ctx.send('Character created')


bot.run(TOKEN)

