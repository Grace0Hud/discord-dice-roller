from lib.db import db
import discord
from discord import embeds

class character:
    #constructor
    #demands name and userID arguments, but the others are defaulted to 0 (or in the case of level, 1)
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

    #calculates the proficiency modifier
    def calcProf(self):
        if(self.level >= 1):
            if(self.level >= 5):
                if(self.level >= 9):
                    if(self.level >= 13):
                        if(self.level >= 17):
                            return 6
                        return 5
                    return 4
                return 3
            return 2
    
    #adds the character object to the database
    def addToDB(self):
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
        #adds every value in fields to the embed as an individual field
        #in the order of a name, (such as Str), a value (such as f'{self.str}' + '(' + f'{character.computeMod(self.str)}')
        #and whether it will be displayed as inline or not (true for all of them)
        for name, value, inline in fields: 
            embed.add_field(name = name, value = value, inline=inline)
        return embed

    #deciding which setter to use, returns false if an invalid value was passed in
    #otherwise updates the stat for the character and the database
    def setStat(self, stat: str, newValue:int):
        if stat == "level":
            self.setLevel(newValue)
        elif stat == "str":
            self.setSt(newValue)
        elif stat == "dex":
            self.setDex(newValue)
        elif stat == "con":
            self.setCon(newValue)
        elif stat == "intel":
            self.setIntel(newValue)
        elif stat == "wis":
            self.setWis(newValue)
        elif stat == "cha":
            self.setCha(newValue)
        else:
            print("Not a valid stat")
            return False
        return True

    #all setters for the class variables, 
    #will update in the database as well. 
    def setLevel(self, newLevel: int):
        self.level = newLevel
        db.execute('UPDATE characterLists SET ChaName = ? WHERE UserID = ?', newLevel, self.userID)
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
        if stat == "str":
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
        elif stat == ' ':
            #this is here for the rol function, 
            #since if it contains the default value
            #there is no need to send an error message
            return None
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
    