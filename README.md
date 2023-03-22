# Mother-ROM-Editor
Work-in progress editor to make ROM Hacking less of a nightmare.

# HOW TO USE:

Just run the python program. You need Python 3.
All of the txt files are required for the program, since it gets the strings (names) of the things from their respective .txt file.
You can edit them to your liking, though. Just make sure to not mess up the ordering, because the program doesn't check for any misplaced names.

There needs to be a file called "Mother.nes" in the same folder as the program & the .txts. Any ROM will do.

# THINGS IT CAN DO:
  - Read items data, show price & users
  
  - Read PSI data
  - Change Level learned of PSI for Ninten and Ana
    - If the PSI Level is set to 1, make the character start with the move. Else, they don't start with the move.
    - Set Level to greater than 99 to remove it from a character's learnset.
    
  - View Enemy Data (their types aren't shown, yet)
  - View and Edit individual enemy data
    - Shows all Stats, Dropped Item, Resistances/Immunities, and their 8 Battle Actions
    - Can Edit HP, PP, Off, Def (untested)
    - Can edit Dropped Item (works)
    - Can edit Resistances (works)
   
  - Shop Editor option (does nothing lol)
  
 
 * Also, case-ing does not matter. You can type in all lowercase and the program will work.
