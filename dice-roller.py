# bot.py
import os
import random
import discord
import random
import dotenv
import asyncio

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
description = '''A dice rolling and character keeping bot for Dungeons and Dragons'''
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
@bot.command(brief = 'paremeters: [sides: a whole number] [#rolls: a whole number]', description = 'Gets a random number between 1 and \'sides\' \'rolls\' times then adds them up and returns them', name='roll')
async def roll(ctx, sides: int, times: int):
    #ctx refers to the context for the channel where the command was sent from
    sum = 0
    for i in range(0, times):
        sum += random.randint(1,sides)
    await ctx.send(sum)

@bot.command(brief = 'paremeters: NONE or [character name]', description = 'Will return all of the characters associated with the caller\'s UserID or a specific character when [character name] is specified', name = 'showchar')
async def showchar(ctx, charaName = ' '):
    #will print out the character information as an embed 
    userID = ctx.author.id

    if(db.record('SELECT ChaName FROM characterLists WHERE UserID = ?', userID) is None):
        await ctx.send("You do not have any characters to show.\n To create one, type \'!newcha [character name]\'")
    elif(charaName == ' '):
        #processing all the characters related to the user ID
        charaList = character.processMultiple(userID, db.records('SELECT ChaName FROM characterLists WHERE userID = ?', userID))
        #creating an embed for each of the characters and storing it in a list
        embedList = [charaList[i].createEmbed() for i in range(0, len(charaList))]
        #list of the emoji reactions to be added to the message
        buttons = [u"\u23EA", u"\u25C0", u"\u25B6",u"\u23E9"]
        current = 0
        msg = await ctx.send(embed=embedList[current])
        
        #adds the buttons as a reaction in the message
        for button in buttons: 
            await msg.add_reaction(button)
        
        #while loop that will be broken out of at time out
        while True:
            try: 
                #checks that the reaction that was added was on of the buttons
                #and that the reaction was done by the author of the command
                #then sets the time out to 60 sec
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout = 60.0)
            #sends the timeout error and removes the reactions.
            except asyncio.TimeoutError:
                embed = embedList[current]
                embed.set_footer(text = "Timed Out.")
                await msg.clear_reactions()

            else:
                previous_page = current
                
                #checks which of the buttons was pressed and reacts accordingly
                if reaction.emoji == u"\u23EA":
                    current = 0
                elif reaction.emoji == u"\u25C0":
                    if current > 0:
                        current -= 1
                elif reaction.emoji == u"\u25B6":
                    if current < len(embedList)-1:
                        current +=1
                elif reaction.emoji == u"\u23E9":
                    current = len(embedList)-1
            
            #removes the reaction after the tesk was completed
            for button in buttons: 
                await msg.remove_reaction(button, ctx.author)
            
            #edits the message with the new embed
            if current != previous_page:
                await msg.edit(embed = embedList[current])

    elif(db.record('SELECT ChaName FROM characterLists WHERE UserID = ? AND ChaName =?', userID, charaName) is None):
        await ctx.send("You don't have a character by that name")
    else:
        chara = character.process(userID, charaName)
        await ctx.send(embed=chara.createEmbed())

@bot.command(brief = 'paremeters: [character name]; optional params: [level] [str] [dex] [con] [int] [wis] [cha]', description = 'Creates a new character by the given name with default stats',name = 'newchar')
async def newcha(ctx, chaName: str, level = 1, st = 0, dex = 0, con = 0, intel = 0, wis = 0, cha = 0):
    userID = ctx.author.id
    #checks to see if there is already a character created for the individual
    #if there isn't, creates the character, if there is it warns them they 
    #already have one
    if(chaName is None):
        await ctx.send('Command: !newchar [characterName]')
    elif(db.record('SELECT chaName FROM characterLists WHERE UserID = ? AND chaName = ?', userID, chaName) is not None):
        await ctx.send('You already have a character by that name.')
    else:
        chara = character(userID, chaName, level, st, dex, con, intel, wis, cha)
        chara.addToDB()
        await ctx.send('Character created')


bot.run(TOKEN)

