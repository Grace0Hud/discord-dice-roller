from character import character
from lib.db import db

#this file was used for testing various pieces of the project as they were written
#to save time while waiting for the bot to come online

#used to contain my own discordID
userID = 0


# charaList = character.processMultiple(userID, db.records('SELECT ChaName FROM characterLists WHERE userID = ?', userID))
# embedList = [charaList[i].createEmbed() for i in range(0, len(charaList))]

chara = character(userID, 'Morn', 12, 2, 3, 5, 6, 20)
print(chara)
chara.setStat('str', 20)
print(chara)
print(chara.getModifier('str'))

