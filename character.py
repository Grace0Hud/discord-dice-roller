class character:
    name = ""
    str = 0
    dex = 0
    con = 0
    intel = 0
    wis = 0
    cha = 0
    #constructors, overloaded
    #takes just the name, then autofills the other values
    # def _init_(self, name):
    #     self.name = name
        # self.str = 0
        # self.dex = 0
        # self.con = 0
        # self.intel = 0
        # self.cha = 0
    #takes the name and all stat values and fills them all
    def __init__(self, name, str=0, dex=0, con=0, intel=0, wis=0, cha=0):
        self.name = name
        self.str = str
        self.dex = dex
        self.con = con
        self.intel = intel
        self.wis = wis
        self.cha = cha
    
    #the to string function, 
    #returns the object in a formatted string
    def __str__(self):
         return f"{self.name}\nstr:{self.str}\ndex:{self.dex}\ncon:{self.con}\nintel:{self.intel}\nwis:{self.wis}\ncha:{self.cha}"
    