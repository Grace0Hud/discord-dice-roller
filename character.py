from lib.db import db
import discord
from discord import embeds

class character:
    #constructor
    #demands a name argument, but the others are defaulted to 0
    def __init__(self, userID:int, name:str, str=0, dex=0, con=0, intel=0, wis=0, cha=0):
        self.name = name
        self.str = str
        self.dex = dex
        self.con = con
        self.intel = intel
        self.wis = wis
        self.cha = cha
    #queries the records associated with the userID and returns a character object with the same information
    def process(userID: int, charaName: str):
        characterInfo = db.record('SELECT * FROM characterLists WHERE UserID = ? AND ChaName = ?', userID, charaName)
        chara = character(characterInfo[0],characterInfo[1],characterInfo[2], characterInfo[3],characterInfo[4],characterInfo[5],characterInfo[6],characterInfo[7])
        return chara
    
    #processes a list of strings of names
    #and returns corresponding character objects
    def processMultiple(userID: int, nameList:list):
        charaList = ['' for i in nameList]
        for i in range(0, len(nameList)):
            charaList[i] = character.process(userID, nameList[i][0])
        return charaList
    def createEmbed(self):
        embed = discord.Embed(title= f'{self.name}', description="You have a character")
        fields = [("Str", f'{self.str}', True),
                ("Dex", f'{self.dex}', True),
                ("Con", f'{self.con}', True),
                ("Int", f'{self.intel}', True),
                ("Wis", f'{self.wis}', True),
                ("Cha", f'{self.cha}', True)]
        for name, value, inline in fields: 
            embed.add_field(name = name, value = value, inline=inline)
        return embed
    #all setters for the class variables, 
    #will update in the database as well. 
    def setName(self, userID: int, newName: str):
        self.name = newName
        db.execute('UPDATE characterLists SET ChaName = ? WHERE UserID = ?', newName, userID)
    def setSt(self, userID: int, newSt: int):
        self.str = newSt
        db.execute('UPDATE characterLists SET st = ? WHERE UserID = ?', newSt, userID)
    def setDex(self, userID: int, newDex: int):
        self.dex = newDex
        db.execute('UPDATE characterLists SET dex = ? WHERE UserID = ?', newDex, userID)    
    def setCon(self, userID: int, newCon: int):
        self.con = newCon
        db.execute('UPDATE characterLists SET con = ? WHERE UserID = ?', newCon, userID)
    def setIntel(self, userID: int, newIntel: int):
        self.intel = newIntel
        db.execute('UPDATE characterLists SET intel = ? WHERE UserID = ?', newIntel, userID)
    def setWis(self, userID: int, newWis: int):
        self.wis = newWis
        db.execute('UPDATE characterLists SET wis = ? WHERE UserID = ?', newWis, userID)
    def setCha(self, userID: int, newCha: int):
        self.cha = newCha
        db.execute('UPDATE characterLists SET cha = ? WHERE UserID = ?', newCha, userID)

    #the to string function, 
    #returns the object in a formatted string
    def __str__(self):
         return f"{self.name}\nstr:{self.str}\ndex:{self.dex}\ncon:{self.con}\nintel:{self.intel}\nwis:{self.wis}\ncha:{self.cha}"
    