from lib.db import db
import discord
from discord import embeds

class character:
    #constructor
    #demands a name argument, but the others are defaulted to 0
    def __init__(self, userID:int, name:str, level = 1, str=0, dex=0, con=0, intel=0, wis=0, cha=0):
        self.userID = userID
        self.name = name
        self.level = level
        self.str = str
        self.dex = dex
        self.con = con
        self.intel = intel
        self.wis = wis
        self.cha = cha
    #queries the records associated with the userID and returns a character object with the same information
    def process(userID: int, charaName: str):
        characterInfo = db.record('SELECT * FROM characterLists WHERE UserID = ? AND ChaName = ?', userID, charaName)
        chara = character(characterInfo[0],characterInfo[1],characterInfo[2], characterInfo[3],characterInfo[4],characterInfo[5],characterInfo[6],characterInfo[7], characterInfo[8])
        return chara
    
    #processes a list of strings of names
    #and returns corresponding character objects
    def processMultiple(userID: int, nameList:list):
        charaList = ['' for i in nameList]
        for i in range(0, len(nameList)):
            charaList[i] = character.process(userID, nameList[i][0])
        return charaList
    
    def addToDB(self):
        # info = [userID, self.name, self.str, self.dex, self.con, self.intel, self.wis, self.cha]
        # valueset = [(i,) for i in info]
        # print(valueset[0])
        # valueset[0],valueset[1],valueset[2],valueset[3],valueset[4],valueset[5],valueset[6],valueset[7]
        db.execute('INSERT INTO characterLists (UserID, ChaName, level, st, dex, con, intel, wis, cha) VALUES (?,?,?,?,?,?,?,?,?)', self.userID, self.name, self.level, self.str, self.dex, self.con, self.intel, self.wis, self.cha)
    
    #creates a formatted embed for the character
    def createEmbed(self):
        embed = discord.Embed(title= f'{self.name}', description='Level: ' + f'{self.level}')
        fields = [("Str", f'{self.str}' + '(' + f'{character.computeMod(self.str)}' + ')', True),
                ("Dex", f'{self.dex}' + '(' + f'{character.computeMod(self.dex)}' + ')', True),
                ("Con", f'{self.con}' + '(' + f'{character.computeMod(self.con)}' + ')', True),
                ("Int", f'{self.intel}' + '(' + f'{character.computeMod(self.intel)}' + ')', True),
                ("Wis", f'{self.wis}'+ '(' + f'{character.computeMod(self.wis)}' + ')', True),
                ("Cha", f'{self.cha}'+ '(' + f'{character.computeMod(self.cha)}' + ')', True)]
        for name, value, inline in fields: 
            embed.add_field(name = name, value = value, inline=inline)
        return embed
    #all setters for the class variables, 
    #will update in the database as well. 
    def setName(self, newName: str):
        self.name = newName
        db.execute('UPDATE characterLists SET ChaName = ? WHERE UserID = ?', newName, self.userID)
    def setLevel(self, newLevel:int):
        self.level = newLevel
        db.execute('UPDATE characterLists SET level = ? WHERE UserID = ?', newLevel, self.userID)
    def setSt(self, newSt: int):
        self.str = newSt
        db.execute('UPDATE characterLists SET st = ? WHERE UserID = ?', newSt, self.userID)
    def setDex(self, newDex: int):
        self.dex = newDex
        db.execute('UPDATE characterLists SET dex = ? WHERE UserID = ?', newDex, self.userID)    
    def setCon(self, newCon: int):
        self.con = newCon
        db.execute('UPDATE characterLists SET con = ? WHERE UserID = ?', newCon, self.userID)
    def setIntel(self, newIntel: int):
        self.intel = newIntel
        db.execute('UPDATE characterLists SET intel = ? WHERE UserID = ?', newIntel, self.userID)
    def setWis(self, newWis: int):
        self.wis = newWis
        db.execute('UPDATE characterLists SET wis = ? WHERE UserID = ?', newWis, self.userID)
    def setCha(self, newCha: int):
        self.cha = newCha
        db.execute('UPDATE characterLists SET cha = ? WHERE UserID = ?', newCha, self.userID)


    #calls compute mod on specified stat
    def getModifier(self, stat: str):
        if stat == "st":
            return character.computeMod(self.str)
        elif stat == "dex":
            return character.computeMod(self.dex)
        elif stat == "con":
            return character.computeMod(self.con)
        elif stat == "intel":
            return character.computeMod(self.intel)
        elif stat == "wis":
            return character.computeMod(self.wis)
        elif stat == "cha":
            return character.computeMod(self.cha)
        else:
            print("Not a valid stat")
            return None

    #computes modifier for stats
    def computeMod(stat:int):
        if stat >= 10:
            return int((stat-10)/2)
        else:
            return int((stat-11)/2)
    #the to string function, 
    #returns the object in a formatted string
    def __str__(self):
         return f"{self.name}\nstr:{self.str}\ndex:{self.dex}\ncon:{self.con}\nintel:{self.intel}\nwis:{self.wis}\ncha:{self.cha}"
    