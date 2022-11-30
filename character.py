from lib.db import db

class character:
    #constructor
    #demands a name argument, but the others are defaulted to 0
    def __init__(self, userID, name, str=0, dex=0, con=0, intel=0, wis=0, cha=0):
        self.name = name
        self.str = str
        self.dex = dex
        self.con = con
        self.intel = intel
        self.wis = wis
        self.cha = cha
    def process(userID):
        characterInfo = db.record('SELECT * FROM characterLists WHERE UserID = ?', userID)
        chara = character(characterInfo[0],characterInfo[1],characterInfo[2], characterInfo[3],characterInfo[4],characterInfo[5],characterInfo[6],characterInfo[7])
        return chara
    #the to string function, 
    #returns the object in a formatted string
    def __str__(self):
         return f"{self.name}\nstr:{self.str}\ndex:{self.dex}\ncon:{self.con}\nintel:{self.intel}\nwis:{self.wis}\ncha:{self.cha}"
    