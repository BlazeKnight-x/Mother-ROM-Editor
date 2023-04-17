# Mother-ROM-Editor
Work-in progress editor to make ROM Hacking less of a nightmare.

# HOW TO USE:

Just run the python program. You need Python 3.
All of the txt files are required for the program, since it gets the strings (names) of the things from their respective .txt file.
You can edit them to your liking, though. Just make sure to not mess up the ordering, because the program doesn't check for any misplaced names.

There needs to be a file called "Mother.nes" in the same folder as the program & the .txts. Any ROM will do. If you want to change this, its a constant on the top of the python file.

# THINGS IT CAN DO:
  - Read/Edit items data: price, Flags (users, edible, key), Actions
  
  - Read PSI data
  - Change Level learned of PSI for Ninten and Ana
    - If the PSI Level is set to 1, make the character start with the move. Else, they don't start with the move.
    - Set Level to greater than 99 to remove it from a character's learnset.
    
  - View Enemy Data (their types aren't shown)
  - View and Edit individual enemy data
    - Shows all Stats, Dropped Item, Resistances/Immunities, and their 8 Battle Actions
    - Can Edit HP, PP, Off, Def
    - Can edit Dropped Item (works)
    - Can edit Resistances (works)
   
  - Character Stats Viewer/Editor
    - Can change Growth Stats and make the initial stats set to match the original style (Growth + 1, or 2 levels of average).
  
  - Shop Viewer/Editor
    - Can input items as hex IDs or user defined strings
  
  - Gift Object Editor
    - Can change the items that certain NPCs give you.
 
 * Also, case-ing does not matter. You can type in all lowercase and the program will work.


# THE OTHER FILE:
 - Auto-Writes Item and Enemy Descriptions, Names of Everything
 - Can be used to translate text to Hex
 - Can calculate Name Pointers given an Offset
