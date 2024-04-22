# Mother-ROM-Editor
Work-in progress editor to make ROM Hacking less of a nightmare.

# HOW TO USE MotherROMEditor.py:

Just run the python program.
InternalStrings folder contains strings that the program uses. The file names are all defined on the top of the python program. You can edit them to your liking.
There needs to be a rom file in the same folder as the program. Any ROM will do. The name is a constant on the top of the python file.

# THINGS IT CAN DO:
  - Read/Edit items data: price, Flags (users, edible, key), set Action ID (cannot edit them, use ASM to do that)
  
  - Read PSI data
  - Edit PSI Action IDs (can't edit overworld actions, use ASM to do that)
  - Change Level learned of PSI for Ninten and Ana
    - If the PSI Level is set to 1, make the character start with the move. Else, they don't start with the move.
    - Set Level to greater than 99 to remove it from a character's learnset.
    
  - View and Edit individual enemy data
    - Show/Edit all Stats, Dropped Item, Resistances/Immunities, and their 8 Battle Actions

  - View and Edit Enemy Groups, Encounter Table groups (cannot edit encounter rate or locations of the Tables).

  - Shop Viewer/Editor
    - Edit the vanilla shops' items. Cannot create new shops or remove existing ones, or edit what objects they use.
   
  - Character Stats Viewer/Editor
    - Can change Growth Stats for Characters 1~5 (Ninten ~ Pippi).
  - Gift Object Editor
    - Can change the items that certain NPCs give you.
 
 * Also, case-ing does not matter. You can type in all lowercase and the program will work.

