# Discord Dice Roller

**CURRENTLY DOWN**  

## How to add to a server
- click this ![link](https://discord.com/api/oauth2/authorize?client_id=1033118243931562045&permissions=8&scope=bot) to be redirected to the authorization page.
- sign in with a discord account
- add the bot to a server in which you have admin permissions

## Command Master List
*commands use "!" prefix*

### Dice Rolling
- roll [sides] [#rolls]
  - the number of sides for the die
  - the number of times it needs to be rolled
  - *ex "roll 6 4" would roll a 6 sided die 4 times and return the result*
- roll [sides] [#rolls] [name] [stat] [proficiency]
  - name: the name of the character to roll for
  - stat: the stat to roll for (which modifier should be used)
  - proficiency: chose from {0, 1, 2}
    - 0: no proficiency
    - 1: proficiency
    - 2: expertise (double proficiency)
  - *ex "roll 20 1 Chiko dex 2" would roll a 20 sided die once, then add Chiko's dexterity modifier, then add double proficiency based on Chiko's level*

### Character Administration
- showchar
  - returns all character sheets associated with the account that sent the command
  - this is presented as a scrollable embed
- showchar [name]
  - name: the name on the character sheet to be returned (case sensitive)
  - returns a character sheet
- newchar [name]
  - name: the name of the character
  - creates a default character sheet.
    - level = 1
    - all stats = 0
- newchar [name] [level] [str] [dex] [con] [int] [wis] [char]
  - name: the name of the character
  - level: the character's current level
  - str: the value of the strength stat
  - dex: the value of the dexterity stat
  - con: the value of the constitution stat
  - int: the value of the intelligence stat
  - wis: the value of the wisdom stat
  - char: the value of the charisma stat
  - any number of stats can be set (for example, only level or only level, str, and dex) but the stats will be set in order.
    - *ex: "newchar Qatu 5" will always set level = 5, not any other stat*
  - the name value is required
  - *ex: "newchar Hjala 7 8 9 0 8 2 0" would create a new character named "Hjala" with stats {level=7, str=8, dex=9, con=0, int=8, wis=2, char=0}*
- updatestat [name] [stat] [value]
  - name: the name of the character
  - stat: the stat to be updated
  - value: the new value of the stat
  - *ex: "updatestat Hjala char 20" would bring Hjala's charisma stat from a dissmal 0 to a skillful 20*
- deletechar [name]
  - name: the name of the character
  - removes the character by the specified name from the user's character sheets
  - *ex: "deletechar Qatu" would permenantly delete Qatu's character sheet*
