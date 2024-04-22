import os
ROOT = os.path.dirname(__file__) + "\\"

### FOLDERS ###
rom_name = "Mother Prime.nes"
FOLDER_INTERNAL = ROOT + '\\InternalStrings'
FOLDER_TEXTTOOL = 'TextTool'
FOLDER_DATA = "Data"
FOLDER_DUMPS = "Dumps"

### DIRECTORIES ###
DIR_ROM = ROOT + '\\' + rom_name

# Internal Names
DIR_ITEMNAME = FOLDER_INTERNAL + "\\ItemStrings.txt"
DIR_PSINAME = FOLDER_INTERNAL + "\\PSIStrings.txt"
DIR_BANAME = FOLDER_INTERNAL + "\\BAStrings.txt"
DIR_PRESENT = ROOT + FOLDER_DATA + "\\Presents.txt"
DIR_ENEMYGROUPNAME = FOLDER_INTERNAL + "\\EnemyGroupStrings.txt"
DIR_BA = ROOT + FOLDER_DATA + "\\BattleActions.txt"

DIR_ENEMYDUMP = ROOT + FOLDER_DUMPS + "\\EnemyDump.txt"
DIR_FULLENEMYDUMP = ROOT + FOLDER_DUMPS + "\\MotherEnemies.csv"

# real Names
DIR_ENEMYNAME = ROOT + FOLDER_TEXTTOOL + "\\Strings\\EnemyName.txt"

#DIR_BANAME = ROOT + FOLDER_INTERNAL + "\\BAStringsV.txt"

### CONSTANTS ###

ITEM_POS = 0x01810
PSI_POS = 0x01E10

GROWTH_POS = 0x1dd8
INITIAL_STATS_POS = 0x31e50

INITIAL_NINTEN_PSI_POS = 0x31e80
INITIAL_ANA_PSI_POS = 0x31ec0

ENEMY_POS = 0x2c010
ENEMY_DATA_LENGTH = 32 #in bytes

ITEM_DESC_POS = 0x30bc8
ITEM_PTR_LENGTH = 3

BATTLE_TEXT_POS = 0x311ad

### GLOBALS ###
ITEMS_ARRAY = []
PSI_ARRAY = []
ENEMY_ARRAY = []
BATTLE_ARRAY = []
PLAYER_ARRAY = []

SHOPS_ARRAY = [ ("Drugs", 0x22a36), ("Fast Food", 0x229b1),
                ("Mother Sports" , 0x23153), ("Mother Food" , 0x2319a),
                ("Magicant Coins" , 0x254f7), ("Magicant Bands" , 0x2553e), ("Magicant Pendants" , 0x25585),
                ("Thanks Sports" , 0x22b69), ("Thanks Food" , 0x22bb0), ("Thanks Misc" , 0x22e50),
                ("Twinkle Scientist" , 0x239dd), ("Snowman" , 0x23258), ("Easter" , 0x22b22),
                ("Reindeer Sports" , 0x22bf7), ("Reindeer Food" , 0x22c3e), ("Reindeer Misc" , 0x22da1),
                ("Valentine Food" , 0x22ea0), ("Valentine Misc" , 0x22c91) ]

ITEM_OBJECTS_ARRAY = [  ("Magic Candy Cat", 0x25064), ("Magic Ribbon Cat", 0x2502D),
                        ("Sweet Little Bin", 0x2466F),
                        ("Tofu Scientist", 0x240d6), ("Assistant B", 0x24128) ]

###########################
### ENCOUNTERS GLOBALS ###
###########################
ENEMY_GROUPS_ARRAY = []
ENCOUNTER_GROUPS_STRINGS = ["Basement", "Mothers", "Yard", "Zoo", "Mothers 2", "Thanksgiving", "Tracks", "Halloween 1",
                            "Snowman", "Easter", "Desert", "Swamp", "Valentine", "Mansion 1", "Mansion 2", "Mansion 3",
                            "Zoo Office", "Duncans 1", "Duncans 2", "Mansion 4", "Sweets 1", "Sweets 2",
                            "Itoi Base", "Itoi Peak", "Itoi Caves", "Itoi Lake", "Magicant", "Cavern"]
ENCOUNTER_TABLE_ARRAY = []

ENEMY_GROUPS_OFFSET = 0x2CFA8
ENEMY_GROUPS_COUNT = 165 #Enemy Group Len = 10
ENEMY_GROUPS_LENGTH = 10

ENEMY_GROUP_POSITIONS = ["Single", "Single", "Single starting 2", "Single starting 2", "Double starting 2", "Triple starting 2", "Triple starting 2",
                         "Double", "Double", "Double", "Triple", "Triple", "Quads", "Quads", "Double Robogirl + Fuel, Distorto + Robo"]

ENCOUNTER_GROUPS_OFFSET = 0x29210
ENCOUNTER_GROUPS_COUNT = 32 #Encounter Group Len = 16
ENCOUNTER_GROUPS_LENGTH = 16
###########################

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #

#####################################################################################################
### Classes ------------------------------------------------------------------------------------- ###
#####################################################################################################

class Item():
    def __init__(self, id, name, flags, equipdata, overworld, battleaction, price, names):
        self.ID = id
        self.namePtr = name
        self.flags = flags
        self.equipData = equipdata
        self.overworld = overworld
        self.battle = battleaction
        self.price = int(price, 16)
        
        self.names = names

    def getBytes(self):
        return self.namePtr + self.flags + self.equipData + self.overworld + self.battle
    def getOverworldAction(self):
        return self.overworld
    def getBattleAction(self):
        return self.battle

    def getID(self):
        if self.ID == '':
            return '0'
        return self.ID
    def getName(self):
        return self.names[0]
    def isName(self, name):
        return name.lower() in (string.lower() for string in self.names)
    # Price
    def getPrice(self):
        return self.price
    # 2 - Flags
    # Droppable?, Edible?, Unused, Pippi, Teddy, Lloyd, Ana, Ninten
    def isKey(self):
        return getBit(self.flags, 0) == 1
    def isEdible(self):
        return getBit(self.flags, 1) == 1
    def getUsers(self):
        # Return as Ninten, Ana, Lloyd, Teddy, Pippi in BOOLEANS
        bits = getBits(self.flags)
        return [bits[7], bits[6], bits[5], bits[4], bits[3]]
    def getUsers(self):
        bit = getBits(self.flags)
        output = ''
        if bit[7]:
            output += ' Ninten'
        if bit[6]:
            output += ' Ana'
        if bit[5]:
            output += ' Lloyd'
        if bit[4]:
            output += ' Teddy'
        if bit[3]:
            output += ' Pippi'
        return output
    def canUse(self, user):
        bit = getBits(self.flags)
        if user == 1 or user.lower() == 'ninten':
            return bit[7]
        elif user == 2 or user.lower() == 'ana':
            return bit[6]
        elif user == 3 or user.lower() == 'lloyd':
            return bit[5]
        elif user == 4 or user.lower() == 'teddy':
            return bit[4]
        elif user == 5 or user.lower() == 'pippi':
            return bit[3]
        else:
            return False
    
    # 3 - EquipData
    # 0, 1 - Type, 2~7 - Attack-Defense-Resistances
    def getType(self):
        bit = getBits(self.equipData)
        equipType = bit[0] + bit[1]
        if equipType == 0:
            if self.isKey():
                return "Key"
            else:
                return 'Weapon'
        elif equipType == 1:
            return "Coin"
        elif equipType == 2:
            return "Bracelet"
        elif equipType == 3:
            return "Pendant"
        else:
            print("There was a grave error in Item.getType() for Item ID:" + self.ID)
            print("For some reason, the bits for type added up to " + equipType)
            return "ERROR GETTING TYPE!"
    def getStats(self):
        bit = getBits(self.equipData)

        output = ''
        if self.getType() == 'Pendant':
            output = 'Pendant'
            # Resistances: 0 = Freeze, 1 = Fire, 2 = Thunder
            if bit[2]:
                output += "\nResists Freeze"
            if bit[3]:
                output += "\nResists Fire"
            if bit[4]:
                output += "\nResists Thunder"
        elif self.getType() == 'Coin' or self.getType() == 'Bracelet':
            output += self.getType() + '\nDefense: ' + (str)(32*bit[2] + 16*bit[3] + 8*bit[4] + 4*bit[5] + 2*bit[6] + bit[7])
        elif self.getType() == 'Weapon':
            output += 'Weapon\nAttack: ' + (str)(32*bit[2] + 16*bit[3] + 8*bit[4] + 4*bit[5] + 2*bit[6] + bit[7])
        return output

class PSI():
    def __init__(self, id, name, pp, ninten, ana, overworld, battle):
        self.ID = id
        self.PP = pp
        self.ninten = ninten
        self.ana = ana
        self.overworldAction = overworld
        self.battleAction = battle
        self.name = name

    def getID(self):
        if self.ID == '':
            return '0'
        return self.ID
    def getPP(self):
        return self.PP
    def getActionIDs(self):
        return self.overworldAction + " " + self.battleAction
    def getOverworldActionID(self):
        return self.overworldAction
    def getBattleActionID(self):
        return self.battleAction
    def getName(self):
        return self.name
    def getNinten(self):
        return self.ninten + 1
    def getAna(self):
        return self.ana + 1
    def getNintenStr(self):
        if self.ninten == 255:
            return ""
        return (str)(self.getNinten())
    def getAnaStr(self):
        if self.ana == 255:
            return ""
        return (str)(self.getAna())
    def isName(self, input):
        name = ''
        for c in input:
            if c == '1':
                name += 'Alpha'
            elif c == '2':
                name += 'Beta'
            elif c == '3':
                name += 'Gamma'
            elif c == '4':
                name += 'Pi'
            elif c == '5':
                name += 'Omega'
            else:
                name += c

        # Try again if the π was 4 and it failed
        if not name == self.name and 'Pi' in name:
            return self.isName(name[:len(name)-2] + 'Omega')
        return name.lower() == self.name.lower()

# All Data is received as bytes (hex Strings) unedited.
class Enemy():
    def __init__(self, id, flags, hp, pp, offense, defense, core, attacks, exp, cash, item, name, location):
        self.location = location

        self.id = id
        self.flags = flags
        self.exp = int.from_bytes(bytes.fromhex(exp), byteorder='little')
        self.money = int.from_bytes(bytes.fromhex(cash), byteorder='little')
        self.item = item
        self.name = name

        self.Core = core
        self.attacks = attacks

        # Complex Data
        self.hp = bytesToBinstr(hp, 'little')
        self.pp = bytesToBinstr(pp, 'little')
        self.Off = bytesToBinstr(offense, 'little')
        self.Def = bytesToBinstr(defense, 'little')

        # Split Binstr #
        # HP
        self.graphic_tile = self.hp[:4]
        self.sub_palette = self.hp[4:6]
        self.hp = self.hp[6:]
        # PP
        self.extra_gfx = self.pp[:6]
        self.pp = self.pp[6:]
        # Off
        self.altitude = self.Off[:3]
        self.deathAction = self.Off[3:6]
        self.Off = self.Off[6:]
        # Def
        self.defeatMsg = self.Def[:6]
        self.Def = self.Def[6:]

    def getLocation(self):
        return self.location
    def getID(self):
        return self.id
    def getName(self):
        return self.name
    def isName(self, str):
        return self.name.lower() == str.lower()
    def getItem(self):
        return getItemName(self.item)
    def getMoney(self):
        return self.money
    def getExp(self):
        return self.exp
    
    def getHP(self):
        return int(self.hp, 2)
    def getPP(self):
        return int(self.pp, 2)
    def getOff(self):
        return int(self.Off, 2)
    def getDef(self):
        return int(self.Def, 2)

    def getDeathAction(self):
        return self.deathAction

    def getCores(self):
        output = []
        for stat in self.Core:
            output.append(int(stat, 16))

        return output
    def getFight(self):
        return self.getCores()[0]
    def getSpeed(self):
        return self.getCores()[1]
    def getWisdom(self):
        return self.getCores()[2]
    def getStrength(self):
        return self.getCores()[3]
    def getForce(self):
        return self.getCores()[4]

    def getAttacks(self):
        output = []
        for attack in self.attacks:
            try:
                output.append(BATTLE_ARRAY[int(attack, 16)])
            except Exception:
                output.append('')
        return output

    def getFlagsBin(self):
        return bin(int(self.flags, 16))[2:].zfill(8)

class EnemyGroup():
    # 0, 1 - Enemy ID (FF = None), Enemy Letter + Call
    # 2-3, 4-5, 6,7 = ""
    # 8 - Position, Special Encounters
    # 9 - Palette, Music
    def __init__(self, name, enemy1, enemy2, enemy3, enemy4, position_byte, visual_byte):
        self.name = name
        self.enemy_array = [enemy1, enemy2, enemy3, enemy4]
        self.position_byte = position_byte
        self.palette_hex = visual_byte[1]
        self.music_hex = visual_byte[0]

    def getEnemyArray(self):
        return self.enemy_array
    def getName(self):
        return self.name
    def isName(self, str):
        return self.name.lower() == str.lower()
    def getEnemy1(self):
        out = getEnemyName(self.enemy_array[0][0])
        return "" if out == '-1' else out
    def getEnemy2(self):
        out = getEnemyName(self.enemy_array[1][0])
        return "" if out == '-1' else out
    def getEnemy3(self):
        out = getEnemyName(self.enemy_array[2][0])
        return "" if out == '-1' else out
    def getEnemy4(self):
        out = getEnemyName(self.enemy_array[3][0])
        return "" if out == '-1' else out
    
    def getEnemy1c(self):
        return self.getEnemy1() + '*' if getBits(self.enemy_array[0][1])[0] == 1 else self.getEnemy1()
    def getEnemy2c(self):
        return self.getEnemy2() + '*' if getBits(self.enemy_array[1][1])[0] == 1 else self.getEnemy2()
    def getEnemy3c(self):
        return self.getEnemy3() + '*' if getBits(self.enemy_array[2][1])[0] == 1 else self.getEnemy3()
    def getEnemy4c(self):
        return self.getEnemy4() + '*' if getBits(self.enemy_array[3][1])[0] == 1 else self.getEnemy4()

    def getPositionByte(self):
        return self.position_byte
    def getPosition(self):
        return self.position_byte[1]
    def getSpecials(self):
        return self.position_byte[0]
    def getPalette(self):
        return self.palette_hex
    def getMusicHex(self):
        return self.music_hex
    def getMusic(self):
        if self.music_hex == '2':
            return "Flippant Foe - 2"
        elif self.music_hex == '3':
            return "Dangerous Foe - 3"
        elif self.music_hex == '4':
            return "Hippie Battle - 4"
        else:
            return self.getMusicHex()
    
    def getEnemies(self):
        return self.getEnemy1c().rjust(14) + " | " + self.getEnemy2c().rjust(14) + " | " +  self.getEnemy3c().rjust(14) + " | " +  self.getEnemy4c().rjust(14)

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #
### Helper Functions ###

# Returns Number
def getBit(hex, bit):
    return int(bin(int(hex, 16))[2:].zfill(8)[bit])
    
# Takes in a Byte as Hex and Returns a List of 8 Bits
def getBits(hex):
    binStr =  bin(int(hex, 16))[2:].zfill(8)
    output = []
    for bit in binStr:
        output.append(int(bit))
    return output

def getBits_String(hex):
    if hex == '00':
        return '00000000'
    
    string = bin(int(hex, 16))[2:].zfill(8)
    
    string.lstrip('0b')
    return string

# Given Bytes, Returns a Binary String with padded 0s on left.
def bytesToBinstr(byteStr = str, byteorder = ["big", "little"]):
    if len(byteStr) % 2 == 1:
        byteStr = "0" + byteStr
    
    byteStr = bytes.fromhex(byteStr)
    if byteorder == 'single':
        return bin(int.from_bytes(byteStr))[2:].zfill(8)
    return bin(int.from_bytes(byteStr, byteorder))[2:].zfill(16)

def is_hex(s):
    try:
        int(s, 16)
        return True
    except Exception:
        return False

def getItemID(identifier):
    if is_hex(identifier) and int(identifier, 16) <= 255:
        return identifier
    
    for item in ITEMS_ARRAY:
        if item.isName(identifier):
            return item.getID()
    
    return '-1'

def getItemName(identifier):
    if is_hex(identifier) and int(identifier, 16) <= 255:
        if identifier == 'a6':
            return "Real Rocket"
        elif identifier == 'a7':
            return "TimeMachine"
        return ITEMS_ARRAY[int(identifier, 16)].getName()
    
    for item in ITEMS_ARRAY:
        if item.isName(identifier):
            return item.getName()
    
    return '-1'

def getEnemyName(identifier):
    if is_hex(identifier) and int(identifier, 16) <= 255 and int(identifier, 16) < len(ENEMY_ARRAY):
        if identifier.lower() == 'ff' or identifier == '00':
            return ""

        return ENEMY_ARRAY[int(identifier, 16)].getName()
    
    for enemy in ENEMY_ARRAY:
        if enemy.isName(identifier):
            return enemy.getName()
    
    return '-1'

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #

#####################################################################################################
### Item Functions------------------------------------------------------------------------------- ###
#####################################################################################################
def read_items():
    ITEMS_ARRAY.clear()
    namesFile = open(DIR_ITEMNAME, 'r')

    with open(DIR_ROM, 'rb') as file:
        file.seek(ITEM_POS)

        # Items go from 00 to 7F
        for i in range(0, 127):
            # Bytes 0, 1 - Name
            Name = bytes.hex(file.read(2))
            
            # 2 - Flags
            Flags = bytes.hex(file.read(1))

            # 3 - Equipment Data
            EquipData = bytes.hex(file.read(1))

            # 4, 5 - Overworld, Battle Action
            Overworld = bytes.hex(file.read(1))
            Battle = bytes.hex(file.read(1))

            # 6, 7 - Price
            Price1 = bytes.hex(file.read(1))
            Price = bytes.hex(file.read(1)) + Price1

            ### GET ITEM NAMES ###
            Names = []
            line = namesFile.readline()

            for string in line.split(','):
                Names.append(string.strip())

            ### Process Item information.
            item = Item(hex(i).lstrip('0x'), Name, Flags, EquipData, Overworld, Battle, Price, Names)
            ITEMS_ARRAY.append(item)
    
    namesFile.close()
    return ITEMS_ARRAY

### Item Printer ========================================================================================
def printAllItems():
    print('===========================================')
    print('================ ALL ITEMS ================')
    print('===========================================')

    # ID, Name, Type, Price
    for item in ITEMS_ARRAY:
        itemPrint = item.getID() + ' | '
        
        if item.getName() != '':
            itemPrint += item.getName().ljust(11) + ' |  $' + (str)(item.getPrice())
        print(itemPrint)

def printItem(identifier):
    hexID = ''
    item = 0
    
    if is_hex(identifier) and int(identifier, 16) <= 255:
        hexID = identifier
        item = ITEMS_ARRAY[int(hexID, 16)]
    else:
        for ITEM in ITEMS_ARRAY:
            if ITEM.isName(identifier):
                item = ITEM
                hexID = item.getID()
    
    if item == 0:
        return

    print('\n==============================\n')
    print(hexID + ' | ' + item.getName().ljust(11) + ' |  $' + (str)(item.getPrice()))
    print('------------------------------\n')
    print("Is Key Item? " + (str)(item.isKey()))
    print("Is Edible? " + (str)(item.isEdible()))
    print("Users:" + item.getUsers())
    print("\nOverworld Action: " + item.getOverworldAction())
    print("Battle Action ID: " + item.getBattleAction())
    print("\nRaw Bytes: " + item.getBytes())
    print('\n==============================\n')

### Item Editor ========================================================================================
def editItemPrice(id):
    print('\nEnter in new value for price (as an integer). Keep in mind values greater than 4 digits don\'t appear properly in the shop menus, although all functionality is maintained.')
    print('You can also input a negative integer to escape.\n')
    Input = ''
    try:
        Input = int(input('  >>> '))
    except ValueError:
        print(' That wasn\'t a number... Did nothing.')
        return

    if Input < 0:
        print(' <-- Escaped...')
        return
    elif Input > 65535:
        print(' That value is too large. The input can\'t be larger than 2 bytes (65535 in decimal).')
        return

    BytesToWrite = hex(Input)[2:].zfill(4)

    # Flip the order of bytes
    BytesToWrite = BytesToWrite[2:] + BytesToWrite[:2]

    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ITEM_POS

        offset += int(id, 16) * 8
        offset += 6

        file.seek(offset)

        file.write(bytes.fromhex(BytesToWrite))

        print('\n ===> Successfully edited price!\n')
    
    read_items()
    return

def editItemStats(id):
    instructions_string = ''

    while(True):
        print('===============================================================\n')
        print('\n0 - Weapon\n1 - Coin Slot\n2 - Bracelet Slot\n3 - Pendant\n4 - Set everything to 0\ne - Escape...\n')
        
        TypeInput = input(' >>> ')

        if TypeInput.lower() == 'e':
            return
        elif TypeInput.lower() == '4':
            break
    
        # Weapon
        elif TypeInput == '0':
            instructions_string = 'Enter Offense value of Weapon (as an int):\n'
            break
        elif TypeInput == '1' or TypeInput == '2':
            instructions_string = 'Enter Defense value of Armour (as an int):\n'
            break
        elif TypeInput == '3':
            instructions_string = 'Enter Pendant Bits (6 in length):\nBit 1 - Resists Fire\nBit 2 - Resists Freeze\nBit 3 - Resists Thunder\nBit 4, 5, 6 - Unknown...\n'
            break

    BytesToWrite = ''
    if TypeInput == '4':
        BytesToWrite = int.to_bytes(0, 1, 'little')

    else:
        print(instructions_string)
        StatsInput = input(' >>> ')

        if TypeInput != '3':
            BytesToWrite = bin(int(TypeInput))[2:].zfill(2) + bin(int(StatsInput))[2:].zfill(6)
        
        # Type is Pendant
        else:
            BytesToWrite = bin(int(TypeInput))[2:].zfill(2) + (StatsInput).zfill(6)
        
        BytesToWrite = int.to_bytes(int(BytesToWrite, 2), 1, 'little')


    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ITEM_POS

        offset += int(id, 16) * 8
        offset += 3

        file.seek(offset)

        file.write(BytesToWrite)

        print('\n ===> Successfully edited item\'s stats!\n')
    
    read_items()
    return

def editItemFlags(id):
    while(True):
        print('===============================================================\n')
        print('\ne - Exit\nBit 0 - Is Key?\nBit 1 - Can Eat?\nBit 2 - Nothing...\n3, 4, 5, 6, 7 - Pippi, Teddy, Lloyd, Ana, Ninten\n')
        
        Inputs = input(' >>> ')

        if Inputs.lower() == 'e':
            return

        if len(Inputs) != 8:
            break

        try:
            Inputs = int(Inputs, 2)
        except Exception:
            break

        # Find the offset.
        with open(DIR_ROM, 'r+b') as file:
            offset = ITEM_POS

            offset += int(id, 16) * 8
            offset += 2

            file.seek(offset)

            file.write(int.to_bytes(Inputs, 1, 'little'))

            print('\n ===> Successfully edited item\'s flags!\n')
        
        read_items()
        return

def editItemActions(id):
    while(True):
        print('===============================================================\n')
        print("\ne - Exit\n0 - Overworld Action (probably don't touch)\n1 - Battle Action\n")
        
        Inputs = input(' >>> ')

        if Inputs.lower() == 'e':
            return

        ActionType = 0

        if Inputs == '1':
            ActionType = 1
        elif Inputs != '0':
            print("Invalid Input type...")
            continue

        Byte = ""
        while(True):
            print("\nEnter ID of Action.\n")
            Byte = input(' >>> ')
            
            if not is_hex(Byte):
                print("Invalid Action input...")
            else:
                break

        # Find the offset.
        with open(DIR_ROM, 'r+b') as file:
            offset = ITEM_POS

            offset += int(id, 16) * 8
            offset += 4 + ActionType

            file.seek(offset)

            file.write(bytes.fromhex(Byte))

            print('\n ===> Successfully edited item\'s action!\n')
        
        read_items()
        return

### Item Description Ptr Editor! ----------------------------------------------------------------
def editItemDescriptionPtr(id):
    print('Enter in the start of the Item\'s description (in hex). It must be 3 bytes long.\nYou can also input 0 to escape.')
    try:
        Input = int(input('  >>> '), 16)
    except ValueError:
        print(' That wasn\'t a hex number... Did nothing.')
        return

    if Input == 0:
        print(' <-- Escaped...')
        return
    elif Input > 16777215: # FF FF FF
        print(' That value is way too large. The input can\'t be larger than 3 bytes.')
        return

    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ITEM_DESC_POS

        offset += int(id, 16) * 3

        file.seek(offset)

        Input -= 0x60010

        file.write(int.to_bytes(Input, 3, 'little'))

        print('\n ===> Successfully edited item pointer!\n')
    
    read_items()
    return

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #

#####################################################################################################
### PSI Functions ------------------------------------------------------------------------------- ###
#####################################################################################################
def read_psi():
    PSI_ARRAY.clear()
    namesFile = open(DIR_PSINAME, 'r')

    with open(DIR_ROM, 'rb') as file:
        file.seek(PSI_POS)

        for i in range(0, 63):
            # Bytes 0, 1 - NamePtr
            Name = bytes.hex(file.read(2))
            
            # 2, 3 - Ninten, Ana Level
            NintenLevel = bytes.hex(file.read(1))
            AnaLevel = bytes.hex(file.read(1))

            # 4, 5 - Overworld, Battle Action ID (not important to save)
            Overworld = bytes.hex(file.read(1))
            Battle = bytes.hex(file.read(1))

            # 6 (not really used)
            useless = bytes.hex(file.read(1))
            
            # 7 - PP Cost (hard coded slot tied to battle action ID)
            PP = bytes.hex(file.read(1))

            ### GET PSI NAMES ###
            Name = namesFile.readline().strip()

            ### Process PSI information.
            psi = PSI(hex(i).lstrip('0x'), Name, int(PP, 16), int(NintenLevel, 16), int(AnaLevel, 16), Overworld, Battle)
            PSI_ARRAY.append(psi)
    
    namesFile.close()

def printAllPSI():
    print('===========================================')
    print('================= ALL PSI =================')
    print('===========================================')

    # ID, Name, Ninten Level, Ana Level
    for psi in PSI_ARRAY:
        psiPrint = "--------------------\n" + psi.getID() + ' | '
        
        if psi.getName() != '':
            psiPrint += psi.getName().ljust(20) + '| PP: ' + (str)(psi.getPP()) + "\n  | Overworld: " + str(psi.getOverworldActionID()) + "      Battle: " + str(psi.getBattleActionID())
            psiPrint += '\n\n      Ninten | ' + psi.getNintenStr() + '\n         Ana | ' + psi.getAnaStr()
        else:
            psiPrint += '\n\n\n'
        print(psiPrint)

def getPSI_ID(identifier):
    if is_hex(identifier) and int(identifier, 16) <= 255:
        return identifier
    
    for PSI in PSI_ARRAY:
        if PSI.isName(identifier):
            return PSI.getID()
    
    return '-1'

def printPSI(identifier):
    hexID = ''
    psi = 0
    
    if is_hex(identifier) and int(identifier, 16) <= 255:
        hexID = identifier
        psi = PSI_ARRAY[int(hexID, 16)]
    else:
        for PSI in PSI_ARRAY:
            if PSI.isName(identifier):
                psi = PSI
                hexID = psi.getID()
    
    if psi == 0:
        return

    print('\n==============================\n')
    print(psi.getName().ljust(11) + ' | PP: ' + (str)(psi.getPP()) + " | Action ID: " + (str)(psi.getActionIDs()) + '\nNinten Level | ' + psi.getNintenStr() + '\n   Ana Level | ' + psi.getAnaStr())
    print('\n==============================\n')

def changePSILevel(id, who):
    with open(DIR_ROM, 'r+b') as file:
        offset = PSI_POS + (int(id, 16) * 8)

        offset += 1 + who

        file.seek(offset)

        character = 'Ninten'
        if who == 2:
            character = 'Ana'

        print('Enter NULL to escape without changing.\n')
        Level = input('Enter a Level to put for ' + character + ' :  ')

        if Level.upper() == 'NULL':
            return
        elif int(Level) > 99:
            Level = '256'

        Level = int(Level) - 1
        file.write(Level.to_bytes(1, 'big'))

        print('\n ===> CHANGED ' + character + '\'s Level Learned to ' + (str)(Level+1))
    
        if Level == 0:
            changeInitialPSI(id, who, 1)
        else:
            changeInitialPSI(id, who, 0)

    read_psi()

def changeInitialPSI(id, who, yes):
    yes = str(yes)
    with open(DIR_ROM, 'r+b') as file:
        offset = INITIAL_NINTEN_PSI_POS
        character = 'Ninten'

        if who == 2:
            offset = INITIAL_ANA_PSI_POS
            character = 'Ana'
        
        offset += (int)(int(id, 16) / 8)

        file.seek(offset)
        byte = bytes.hex(file.read(1))
        byte = getBits_String(byte)

        byte = list(byte)

        # IF the Bit must be changed, change it and print that it changed.
        if byte[int(id, 16) % 8] != yes:
            byte[int(id, 16) % 8] = yes

            byte = "".join(byte)

            byte = int(byte, 2)

            file.seek(offset)
            file.write(byte.to_bytes(1, 'big'))

            print(' ===> CHANGED ' + character + '\'s Initial Learn to ' + (str)(bool(yes=='1')))

def editPSIAction(id):
    print("0 - Overworld Action, 1 - Battle Action\n")
    action_type = 0
    while(True):
        action_type = input(' >>> ')
        
        if action_type.lower() == '0':
            break
        elif action_type.lower() == '1':
            action_type = 1
            break
        
    action_id = ""

    while(not is_hex(action_id)):
        action_id = input("enter action ID: ")

    with open(DIR_ROM, 'r+b') as file:
        offset = PSI_POS + (int(id, 16) * 8)

        offset += 4 + int(action_type)

        file.seek(offset)

        file.write(bytes.fromhex(action_id))

        print('\n ===> Successfully edited action.')

    read_psi()

def editPSICost(id):
    print("Enter new cost. You can also enter 'e' to escape.\n")
    cost = ''
    while(True):
        cost = input(' >>> ')
        
        if cost.lower() == 'e':
            return
        
        try:
            cost = int(cost)
            break
        except ValueError:
            print("You need to enter an integer, silly...")


    with open(DIR_ROM, 'r+b') as file:
        offset = PSI_POS + (int(id, 16) * 8)

        offset += 7

        file.seek(offset)

        file.write(int.to_bytes(cost, 1, 'little'))

        print('\n ===> Successfully edited cost.')

    read_psi()

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #

#####################################################################################################
### Enemies Functions --------------------------------------------------------------------------- ###
#####################################################################################################

def read_enemies():
    ENEMY_ARRAY.clear()
    namesFile = open(DIR_ENEMYNAME, 'r')

    with open(DIR_ROM, 'rb') as file:
        file.seek(ENEMY_POS)

        # Entries go from 00 to FF? (only 122 used)
        for i in range(0, 122):
            location = hex(file.tell())

            # Bytes 0, 1 - Unused, Initial Status
            bytes.hex(file.read(2))
            
            # 2 - Flags
            Flags = bytes.hex(file.read(1))

            # 3, 4 - HP, Sub-Palette, Graphic Tile Data
            HP = bytes.hex(file.read(2))

            # 5, 6 - PP, Graphics
            PP = bytes.hex(file.read(2))

            # 7, 8 - Offense, Death Action, Height
            Off = bytes.hex(file.read(2))

            # 9, 10 - Defense, Defeat Message, Unknown
            Def = bytes.hex(file.read(2))

            # 11 ~ 15 - Core Stats (Fight, Spd, Wis, Str, Force)
            Cores = []
            for _ in range(5):
                Cores.append(bytes.hex(file.read(1)))

            # 16 ~ 23 - Attacks
            Attacks = []
            for _ in range(8):
                Attacks.append(bytes.hex(file.read(1)))

            # 24, 25 - Name Ptr
            bytes.hex(file.read(2))
            
            # 26, 27 - Exp
            EXP = bytes.hex(file.read(2))

            # 28, 29 - Money
            Cash = bytes.hex(file.read(2))

            # 30 - Item
            ITEM = bytes.hex(file.read(1))

            # 31 - Graphic Tileset
            bytes.hex(file.read(1))

            ### GET Enemy NAME ###
            Name = namesFile.readline().strip()

            ### Process Enemy information.
            enemy = Enemy(hex(i).lstrip('0x'), Flags, HP, PP, Off, Def, Cores, Attacks, EXP, Cash, ITEM, Name, location)
            ENEMY_ARRAY.append(enemy)
    
    namesFile.close()
    read_battle()

def read_battle():
    BATTLE_ARRAY.clear()
    with open(DIR_BANAME, 'r') as file:
        for _ in range(134):
            BATTLE_ARRAY.append(file.readline().strip())

def getEnemyID(identifier):
    if is_hex(identifier) and int(identifier, 16) <= 255:
        return identifier
    
    for e in ENEMY_ARRAY:
        if e.isName(identifier):
            return e.getID()
    
    return '-1'

def getBattleID(identifier):
    if is_hex(identifier) and int(identifier, 16) <= 255:
        s = identifier.zfill(2)
        return s
    
    for i in range(len(BATTLE_ARRAY)):
        if BATTLE_ARRAY[i].lower() == identifier.lower():
            s = hex(i).lstrip('0x')
            return s.zfill(2)
    
    return '-1'

def printAllEnemies():
    print('===========================================')
    print('=============== ALL ENEMIES ===============')
    print('===========================================')
    print('ID | Name         |  HP  |  PP  |  Off |  Def |  Fig |  Spd |  Wis |  Str |  Fce | Item        |  EXP | Money')

    for E in ENEMY_ARRAY:
        enemyPrint = E.getID().rjust(2) + ' | '
        
        if E.getName() != '':
            enemyPrint += (E.getName().ljust(13) + '| ' + str(E.getHP()).rjust(4) + ' | ' + str(E.getPP()).rjust(4) + " | " + str(E.getOff()).rjust(4) + ' | '
                + str(E.getDef()).rjust(4) + " | " + str(E.getFight()).rjust(4) + ' | ' + str(E.getSpeed()).rjust(4) + ' | ' + str(E.getWisdom()).rjust(4) + " | " 
                + str(E.getStrength()).rjust(4) + " | " + str(E.getForce()).rjust(4) + ' | ' + E.getItem().rjust(11) + " | "
                + str(E.getExp()).rjust(4) + " | $" +  str(E.getMoney()))
        
        print(enemyPrint)

def printAllEnemiesByArea(areaFile = str, whatToPrint = int):
    print('===========================================')
    print('=============== ALL ENEMIES ===============')
    print('================= BY AREA =================')

    with open(FOLDER_INTERNAL + "/" + areaFile, 'r') as file:
        for line in file:
            line = line.split(";")
            print("\n" + line[0].strip())
            
            if whatToPrint == 0:
                print('ID | Name         |  HP  |  PP  |  Off |  Def |  Fig |  Spd |  Wis |  Str |  Fce | Item        |  EXP | Money')
            elif whatToPrint == 1:
                print('ID | Name         |  HP  |  PP  |  Off |  Def |  Spd | Stat| Fire| Ice | Elec| null|Mentl|Light|  Bug')
            for identifier in line[1].split(","):
                E = ENEMY_ARRAY[int(getEnemyID(identifier.strip()), 16)]
                enemyPrint = E.getID().rjust(2) + ' | '
                
                if E.getName() != '':
                    if whatToPrint == 0:
                        enemyPrint += (E.getName().ljust(13) + '| ' + str(E.getHP()).rjust(4) + ' | ' + str(E.getPP()).rjust(4) + " | " + str(E.getOff()).rjust(4) + ' | '
                        + str(E.getDef()).rjust(4) + " | " + str(E.getFight()).rjust(4) + ' | ' + str(E.getSpeed()).rjust(4) + ' | ' + str(E.getWisdom()).rjust(4) + " | " 
                        + str(E.getStrength()).rjust(4) + " | " + str(E.getForce()).rjust(4) + ' | ' + E.getItem().rjust(11) + " | "
                        + str(E.getExp()).rjust(4) + " | $" +  str(E.getMoney()))

                    elif whatToPrint == 1:
                        enemyPrint += (E.getName().ljust(13) + '| ' + str(E.getHP()).rjust(4) + ' | ' + str(E.getPP()).rjust(4) + " | " + str(E.getOff()).rjust(4) + ' | '
                        + str(E.getDef()).rjust(4) + " | " + str(E.getSpeed()).rjust(4))
                        
                        flags = E.getFlagsBin()
                        for _ in range(8):
                            enemyPrint += " |   " + flags[_]
                print(enemyPrint)

def printAllEnemiesAttacks():
    print('===========================================')
    print('=============== ALL ENEMIES ===============')
    print('================= ATTACKS =================')

    with open(FOLDER_INTERNAL + "/Enemy Areas.txt", 'r') as file:
        for line in file:
            line = line.split(";")
            print("\n" + line[0].strip())
            print('ID | Name         |')

            for identifier in line[1].split(","):
                E = ENEMY_ARRAY[int(getEnemyID(identifier.strip()), 16)]
                enemyPrint = E.getID().rjust(2) + ' | '
                
                if E.getName() != '':
                    enemyPrint += (E.getName().ljust(13) + '| ' + str(E.getAttacks()))
                print(enemyPrint)

def printEnemy(identifier):
    hexID = ''
    enemy = 0
    
    if is_hex(identifier) and int(identifier, 16) <= 255:
        hexID = identifier
        enemy = ENEMY_ARRAY[int(hexID, 16)]
    else:
        for ENEMY in ENEMY_ARRAY:
            if ENEMY.isName(identifier):
                enemy = ENEMY
                hexID = enemy.getID()
    
    if enemy == 0:
        return

    print('\n==============================\n')
    print("Location: " + enemy.getLocation() + "\n")
    print(enemy.getName().ljust(13) + '\nHP: ' + str(enemy.getHP()) + '\nPP: ' + str(enemy.getPP()) + '\nOff: ' + str(enemy.getOff()) + '\nDef: ' + str(enemy.getDef()))
    cores = enemy.getCores()
    print('Fight: ' + str(cores[0]) + '\nSpeed: ' + str(cores[1]) + '\nWisdom: ' + str(cores[2]) + '\nStrength: ' + str(cores[3]) + '\nForce: ' + str(cores[4]))
    print('Dropped Item: ' + enemy.getItem())
    
    print("\nExperience: " + str(enemy.getExp()))
    print("Money: " + str(enemy.getMoney()))
    print('\n================\nFlags:\n')
    flags = enemy.getFlagsBin()
    adj = 43
        
    print('Immune to Status, Beam \u03b3, Debuffers'.ljust(adj-1) + '| ' + flags[0]
          + '\nResists Fire'.ljust(adj) + '| ' + flags[1] 
          + '\nResists Freeze'.ljust(adj) + '| ' + flags[2]
          + '\nResists Thunder'.ljust(adj) + '| ' + flags[3]
          + '\nUnknown Bit...'.ljust(adj) + '| ' + flags[4]
          + '\nImmune to Sleep/Confuse, Resists Def. Down'.ljust(adj) + '| ' + flags[5]
          + '\nResists Light'.ljust(adj) + '| ' + flags[6]
          + '\nWeak to Bug Spray'.ljust(adj)  + '| '+ flags[7] )

    attacks = enemy.getAttacks()
    print('\n==============================\nAttacks:\n' + str(attacks))
    print('\n==============================\n')

def fulldumpAllEnemies(areaFile = str):
    with open(DIR_FULLENEMYDUMP, "r+") as dump:
        dump.write("ID,Name,HP,PP,Off,Def,Fit,Spd,Wis,Str,Fce,Item,EXP,Money,Actions,,,,,,,Immune to Status,Resist Fire,Resist Ice,Resist Electric,null,Mental Immunity,Resist Light,Weak to Bug Spray")
        with open(FOLDER_INTERNAL + "/" + areaFile, 'r') as file:
            for line in file:
                line = line.split(";")
                #print("\n" + line[0].strip())
                for identifier in line[1].split(","):
                    E = ENEMY_ARRAY[int(getEnemyID(identifier.strip()), 16)]
                    dump.write(E.getID().rjust(2) + ',')
                    
                    if E.getName() != '':
                        dump.write(E.getName().ljust(13) + ',' + str(E.getHP()).rjust(4) + ',' + str(E.getPP()).rjust(4) + ","
                            + str(E.getOff()).rjust(4) + ',' + str(E.getDef()).rjust(4) + ","
                            + str(E.getFight()).rjust(4) + ',' + str(E.getSpeed()).rjust(4) + ',' + str(E.getWisdom()).rjust(4) + "," 
                            + str(E.getStrength()).rjust(4) + "," + str(E.getForce()).rjust(4) + ',' + E.getItem().rjust(11) + ","
                            + str(E.getExp()).rjust(4) + ",$" +  str(E.getMoney()) + ","
                        )

                        for A in E.getAttacks():
                            dump.write(A + ",")

                        flags = E.getFlagsBin()
                        for _ in range(8):
                            dump.write(flags[_] + ",")
                    
                    dump.write("\n")
                        
                dump.write("\n")


                    
        

    

def editBattle(id):
    print('\nEnter in attacks. There must be 8 attacks, and they must be separated by commas. IDs or Names are accepted.\nYou can also input 0 to escape.\n')

    NewAttacks = input('  >>> ')

    if NewAttacks == '0':
        print(' <-- Escaped...')
        return
    
    NewAttacks = NewAttacks.split(',')
    
    if len(NewAttacks) != 8:
        print(' <-- There wasn\'t the right amount of attacks.')
        return
    
    WriteBytes = ''

    for attack in NewAttacks:
        hexID = getBattleID(attack.strip())
        if hexID == '-1':
            print(' <-- There was an invalid attack.')
            return
        WriteBytes += hexID
        
    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_POS

        offset += int(id, 16) * 32
        offset += 16

        file.seek(offset)

        file.write(bytes.fromhex(WriteBytes))

        print('\n ===> Successfully edited attacks!')
    
    read_enemies()

def editEnemyDrop(id):
    print('\nEnter in Item. ID or Names are accepted.\nYou can also input 0 to escape, or -1 to remove the item.\n')

    Input = input('  >>> ')

    ItemID = '00'
    if Input == '0':
        print(' <-- Escaped...')
        return
    elif Input != '-1':
        ItemID = getItemID(Input)
        ItemID = ItemID.strip()
    
    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_POS

        offset += int(id, 16) * 32
        offset += 30

        file.seek(offset)

        file.write(bytes.fromhex(ItemID))

        print('\n ===> Successfully edited item!')
    
    read_enemies()

def editEnemyStat(id, what):
    statString = ''
    binstrHi = ''
    statOffset = ''
    curr: Enemy = ENEMY_ARRAY[int(id, 16)]
    if what == 'hp':
        statString = 'HP'
        binstrHi = curr.graphic_tile + curr.sub_palette
        statOffset = 3
    elif what == 'pp':
        statString = 'PP'
        binstrHi = curr.extra_gfx
        statOffset = 5
    elif what == 'off':
        statString = 'Offense'
        binstrHi =  curr.altitude + curr.deathAction
        statOffset = 7
    elif what == 'def':
        statString = 'Defense'
        binstrHi = curr.defeatMsg
        statOffset = 9
    
    while(True):
        Input = input('\nEnter in new value for ' + statString + ' (as an integer). Cannot be larger than 1023.\nYou can also input -1 to escape.\n')
        if not Input.isdigit():
            print("\tValue inputted was not a number.")
            continue
        Input = int(Input)
        if Input == -1:
            print('\tEscaped...')
            return
        elif Input < 0:
            print('\tThe value cannot be negative, silly.')
        elif Input > 1023:
            print('\tThat value is too large. The input can\'t be larger than 10 bits (1023 in decimal).')
        else:
            break

    # Translate the int into Bits
    inputBinstr = hex(Input).lstrip("0x") # 2 Bytes In Big-endian order

    inputBinstr = bytesToBinstr(inputBinstr, 'big') # Translate 2 Bytes to Binstr of 16
    inputBinstr = binstrHi + inputBinstr[6:]        # Add binstrHi and last 10 Bits

    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_POS

        offset += int(id, 16) * 32
        offset += statOffset

        file.seek(offset)

        file.write(int(inputBinstr[8:], 2).to_bytes(1, 'little'))
        file.write(int(inputBinstr[:8], 2).to_bytes(1, 'little'))

        print('\n ===> Successfully edited ' + statString + '!\n')
    
    read_enemies()

def editEnemyFlags(id):
    print('\nEnter in flags as binary bits in order. There must be 8 bits. Spaces are fine.\nYou can also input a single 0 to escape.\n')

    Input = input('  >>> ')

    if Input == '0':
        print(' <-- Escaped...')
        return
    
    Input = "".join(Input.split())

    if len(Input) != 8:
        print(' Length of the bits was not 8...')
        return
    
    try:
        Input = int(Input, 2)
    except ValueError:
        print(' Input wasn\'t a binary string...')
        return
    
    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_POS

        offset += int(id, 16) * 32
        offset += 2

        file.seek(offset)

        file.write(Input.to_bytes(1, 'big'))

        print('\n ===> Successfully edited flags!')
    
    read_enemies()

def editEnemyCore(id):
    print('\ne - Escape\n1 - Fight\n2 - Speed\n3 - Wisdom\n4 - Strength\n5 - Force\n')

    what = ''

    while True:
        print("Enter value to edit:")
        what = input(' >>> ')

        if what.lower() == 'e':
            return

        try:
            what = int(what)
        except Exception:
            print('Non-proper value received...')

        if what < 1 or what > 5:
            print('Non-proper value received...')

        else:
            break

    Input = input("\ne - Escape\nEnter new value for stat:\n >>> ")

    if Input.lower() == 'e':
        print(' <-- Escaped...')
        return
    
    try:
        Input = int(Input)
    except Exception:
        print('Non-number given...')
        return
    
    if Input < 0 or Input > 255:
        print('Input is not within 0 ~ 255...')
        return

    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_POS

        offset += int(id, 16) * 32
        offset += 10 + what

        file.seek(offset)

        file.write(Input.to_bytes(1, 'big'))

        print('\n ===> Successfully edited stat!')
    read_enemies()

def editEnemyTwoBytes(id):
    print('\ne - Escape\n1 - EXP\n2 - Money\n')

    what = ''

    while True:
        print("Enter value to edit:")
        what = input(' >>> ')

        if what.lower() == 'e':
            return

        try:
            what = int(what)
        except Exception:
            print('Non-proper value received...')

        if what < 1 or what > 2:
            print('Non-proper value received...')

        else:
            break

    Input = input("\ne - Escape\nEnter new value for stat:\n >>> ")

    if Input.lower() == 'e':
        print(' <-- Escaped...')
        return
    
    try:
        Input = int(Input)
    except Exception:
        print('Non-number given...')
        return
    
    if Input < 0 or Input > 0xffff:
        print('Input is not within 2 Bytes...')
        return

    # Find the offset.
    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_POS

        offset += (int(id, 16) * 32) + 24
        offset += what * 2

        file.seek(offset)

        file.write(Input.to_bytes(2, 'little'))

        print('\n ===> Successfully edited value!')
    read_enemies()

# Function to output all Enemy data to a text file
def dumpAllEnemies():
    read_enemies()

    with open(DIR_ENEMYDUMP, "r+") as file:
        file.write("Name,HP,PP,Offense,Defense,Speed,Fight,Wisdom,Strength,Force,EXP,Money,Item,Resists Light,Resists Fire,Resists Freeze,Resists Thunder,Bug Sprayed,Status Resistant,Status Immune")

        for enemy in ENEMY_ARRAY:
            if enemy.getName() != "":
                enemyDump = enemy.getName() + "," + str(enemy.getHP()) + "," + str(enemy.getPP()) + "," + str(enemy.getOff()) + "," + str(enemy.getDef()) + "," + str(enemy.getCores()[1]) + "," + str(enemy.getCores()[0]) + "," + str(enemy.getCores()[2]) + "," + str(enemy.getCores()[3]) + "," + str(enemy.getCores()[4]) + "," + str(enemy.getExp()) + ",$" +  str(enemy.getMoney())+ "," + enemy.getItem()
            
                file.write(enemyDump)
            else:
                file.write("")

#####################################################################################################
### Chara Functions ---------------------------------------------------------------------------- ###
#####################################################################################################
def read_charas():
    PLAYER_ARRAY.clear()

    with open(DIR_ROM, 'rb') as file:
        file.seek(GROWTH_POS)

        # Entries go from 00 to FF? (only 122 used)
        for _ in range(5):
            # Bytes 0, 1 - Name Pointer
            bytes.hex(file.read(2))
            
            # 2 - PSI Level Learned Hex (02 Ninten, 03 Ana)
            bytes.hex(file.read(1))

            # 3, 4, 5, 6, 7 - Core Stats
            Cores = []
            for j in range(5):
                Cores.append(bytes.hex(file.read(1)))

            ### Process Player Growth Stats
            PLAYER_ARRAY.append(Cores)

def printAllCharas():
    read_charas()

    print('Ninten: ' + (str)(PLAYER_ARRAY[0]))
    print('Ana   : ' + (str)(PLAYER_ARRAY[1]))
    print('Lloyd : ' + (str)(PLAYER_ARRAY[2]))
    print('Teddy : ' + (str)(PLAYER_ARRAY[3]))
    print('Pippi : ' + (str)(PLAYER_ARRAY[4]))

def printChara(id_int):
    read_charas()

    print(PLAYER_ARRAY[id_int - 1])

def translateAvgToGrowth(avg):
    return int(2*avg - 1)
def translateMaxToGrowth(max):
    return int(2*(max-0.5) - 1)

def editCharaStat(chara_id, stat_id, input_method):
    stat_name = ''
    if stat_id == 1:
        stat_name = 'Fight'
    elif stat_id == 2:
        stat_name = 'Speed'
    elif stat_id == 3:
        stat_name = 'Wisdom'
    elif stat_id == 4:
        stat_name = 'Strength'
    elif stat_id == 5:
        stat_name = 'Force'
    else:
        print('Some strange error occured in editCharaStat...')
        return

    print('Enter the growth value for ' + stat_name)
    input_stat = input(' >>> ')

    try:
        input_stat = float(input_stat)
    except ValueError:
        print("Didn't receive a number as the stat value...")
        return

    if input_method == 'a':
        input_stat = translateAvgToGrowth(input_stat)
    elif input_method == 'g':
        input_stat = (int)(input_stat)
    elif input_method == '':
        input_stat = translateMaxToGrowth(input_stat)

    if input_stat < 0 or input_stat > 255:
        print("Received a value that isn't within a byte...")
        return

    with open(DIR_ROM, 'r+b') as file:
        offset = GROWTH_POS + 8*(chara_id - 1) + 2 + stat_id
        file.seek(offset)

        file.write(int.to_bytes(input_stat, 1, 'big'))

    editCharaInitStat(chara_id, stat_id)

def editCharaInitStat(chara_id, stat_id):
    stat_name = ''
    if stat_id == 1:
        stat_name = 'Fight'
    elif stat_id == 2:
        stat_name = 'Speed'
    elif stat_id == 3:
        stat_name = 'Wisdom'
    elif stat_id == 4:
        stat_name = 'Strength'
    elif stat_id == 5:
        stat_name = 'Force'
    else:
        print('Some strange error occured in editCharaStat...')
        return

    print('Enter the value for ' + stat_name + '. You can also type "-1" to make it default based on growth stats, or "e" to leave it the same.')
    input_stat = input(' >>> ')

    if input_stat.lower() == 'e':
        return

    try:
        input_stat = int(input_stat)
    except ValueError:
        print("Didn't receive a number as the stat value...")
        return

    if input_stat == -1:
        input_stat = int(PLAYER_ARRAY[chara_id - 1][stat_id - 1], 16) + 1
    
    with open(DIR_ROM, 'r+b') as file:
        offset = INITIAL_STATS_POS + 64*(chara_id - 1) + 10 + stat_id
        file.seek(offset)

        file.write(int.to_bytes(input_stat, 1, 'big'))

        if stat_name == 'Fight' or stat_name == 'Speed':
            offset = INITIAL_STATS_POS + 64*(chara_id - 1) + 5 + (2*stat_id)
            file.seek(offset)

            file.write(int.to_bytes(input_stat, 1, 'big'))

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #

#####################################################################################################
### Shop Functions ---- Object Functions ------------------------------------------------------ ###
#####################################################################################################

def printAllShops():
    i = 0
    print('ID | Shop Name        | Items')
    with open(DIR_ROM, 'rb') as file:
        for name, offset in SHOPS_ARRAY:
            file.seek(offset)
            ids = [bytes.hex(file.read(1))]
            ids.append(bytes.hex(file.read(1)))
            ids.append(bytes.hex(file.read(1)))
            ids.append(bytes.hex(file.read(1)))
            

            print(str(i).rjust(2) + ' | ' + name.ljust(17) + '| ' + getItemName(ids[0]).rjust(11) + ' | ' + getItemName(ids[1]).rjust(11) +' | '
                  + getItemName(ids[2]).rjust(11) + ' | ' + getItemName(ids[3]).rjust(11))

            if(i == 1 or i == 3 or i == 6 or i == 9 or i == 12 or i == 15):
                print("")


            i += 1

def editShops():
    while(True):
        printAllShops()
        print("\nEnter ID / Name of shop to edit, or -1 to escape...")
        input_id = input(" >>> ")

        if input_id == '-1':
            return

        for i in range(len(SHOPS_ARRAY)):
            if input_id.lower() == SHOPS_ARRAY[i][0].lower():
                input_id = i
                break

        try:
            input_id = int(input_id)
        except ValueError:
            print("That wasn't a number...\n\n")
            continue
        
        if input_id < 0 or input_id > len(SHOPS_ARRAY):
            print("That wasn't a valid ID...\n\n")
            continue
        
        print("Now Editing " + SHOPS_ARRAY[input_id][0] + "...\n")
        print("\nEnter 4 items, as string or bytes, separated by commas. ID of '0' means no item. -1 is escape.")
        
        items = input(" >>> ")

        if items == '-1':
            print("Escaped...")
            continue

        items = items.split(',')

        if len(items) > 4:
            print('Received incorrect number of IDs.\n\n')
            continue
        elif len(items) < 4:
            while(len(items) != 4):
                items.append('00')


        BytesToWrite = ''
        for item in items:
            item = item.strip()
            if is_hex(item):
                BytesToWrite += item.zfill(2)
            
            else:
                BytesToWrite += getItemID(item).zfill(2)

        if len(BytesToWrite) != 8:
            print('Received incorrect nummber of identifiers?')
            continue

        with open(DIR_ROM, 'r+b') as file:
            file.seek(SHOPS_ARRAY[input_id][1])

            file.write(bytes.fromhex(BytesToWrite))

            print("\nSuccessfully edited the shop!\n")

def printAllObjects():
    i = 0
    print('ID | Object           | Item')
    with open(DIR_ROM, 'rb') as file:
        for name, offset in ITEM_OBJECTS_ARRAY:
            file.seek(offset)
            item_id = bytes.hex(file.read(1))
            

            print(str(i).rjust(2) + ' | ' + name.ljust(17) + '| ' + getItemName(item_id).rjust(11))

            if(i == 1 or i == 2):
                print("")


            i += 1

def printAllPresents():
    PRESENTS_ARRAY = readPresents()
    print('ID | Object           | Item')
    with open(DIR_ROM, 'rb') as file:
        for id, offset, name in PRESENTS_ARRAY:
            file.seek(offset)
            item_id = bytes.hex(file.read(1))
            print(id + ' | ' + name.ljust(17) + '| ' + getItemName(item_id).rjust(11))

def editObjects():
    while(True):
        printAllObjects()
        print("\nEnter ID / Name of object to edit, or -1 to escape...")
        input_id = input(" >>> ")

        if input_id == '-1':
            return

        for i in range(len(ITEM_OBJECTS_ARRAY)):
            if input_id.lower() == ITEM_OBJECTS_ARRAY[i][0].lower():
                input_id = i
                break

        try:
            input_id = int(input_id)
        except ValueError:
            print("That wasn't a number...\n\n")
            continue
        
        if input_id < 0 or input_id > len(ITEM_OBJECTS_ARRAY):
            print("That wasn't a valid ID...\n\n")
            continue
        
        print("Now Editing " + ITEM_OBJECTS_ARRAY[input_id][0] + "...\n")
        print("\nEnter an item, as string or ID. ID of '0' means no item. -1 is escape.")
        
        input_item = input(" >>> ")

        if input_item == '-1':
            print("Escaped...")
            continue

        BytesToWrite = ''
        
        input_item = input_item.strip()
        if is_hex(input_item):
            BytesToWrite += input_item.zfill(2)
        
        else:
            BytesToWrite += getItemID(input_item).zfill(2)

        if not is_hex(BytesToWrite):
            print('Received incorrect identifier...')
            continue

        with open(DIR_ROM, 'r+b') as file:
            file.seek(ITEM_OBJECTS_ARRAY[input_id][1])

            file.write(bytes.fromhex(BytesToWrite))

            print("\nSuccessfully edited the object!\n")

def readPresents():
    Output = []

    with open(DIR_PRESENT, 'r') as file:
        for line in file.readlines():
            line = line.split(",")
            
            if len(line) != 3:
                continue

            if not is_hex(line[0]):
                continue
            
            line[0] = line[0].strip()
            line[1] = int(line[1], 16)
            line[2] = line[2].strip()
            Output.append(line)

    return Output

def editPresents():
    PRESENTS_ARRAY = readPresents()
    while(True):
        printAllPresents()
        print("\nEnter ID / Name of present to edit, or -1 to escape...")
        input_id = input(" >>> ")

        if input_id == '-1':
            return

        input_id = input_id.lower().strip()

        present = []

        for p in PRESENTS_ARRAY:
            if input_id == p[0] or input_id == p[2].lower():
                present = p
                break

        
        if len(present) == 0:
            print("That wasn't a valid ID...\n\n")
            continue
        
        print("Now Editing " + present[2] + "...\n")
        print("\nEnter an item, as string or ID. ID of '0' means no item. -1 is escape.")
        
        input_item = input(" >>> ")

        if input_item == '-1':
            print("Escaped...")
            continue

        BytesToWrite = ''
        
        input_item = input_item.strip()
        if is_hex(input_item):
            BytesToWrite += input_item.zfill(2)
        
        else:
            BytesToWrite += getItemID(input_item).zfill(2)

        if not is_hex(BytesToWrite):
            print('Received incorrect identifier...')
            continue

        with open(DIR_ROM, 'r+b') as file:
            file.seek(present[1])

            file.write(bytes.fromhex(BytesToWrite))

            print("\nSuccessfully edited the present!\n")

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #

#####################################################################################################
### Enemy Groups Functions ---------------------------------------------------------------------- ###
#####################################################################################################

def read_enemy_groups():
    read_enemies()
    ENEMY_GROUPS_ARRAY.clear()

    namesFile = open(DIR_ENEMYGROUPNAME, "r")
    with open(DIR_ROM, 'rb') as file:
        file.seek(ENEMY_GROUPS_OFFSET)

        for _ in range(ENEMY_GROUPS_COUNT):
            # ENEMY_GROUPS_LENGTH = 10

            # 0, 1; 2, 3; 4, 5; 6, 7 - Enemy Data
            enemy1 = [bytes.hex(file.read(1)), bytes.hex(file.read(1))]
            enemy2 = [bytes.hex(file.read(1)), bytes.hex(file.read(1))]
            enemy3 = [bytes.hex(file.read(1)), bytes.hex(file.read(1))]
            enemy4 = [bytes.hex(file.read(1)), bytes.hex(file.read(1))]

            posByte = bytes.hex(file.read(1))
            visByte = bytes.hex(file.read(1))

            name = namesFile.readline().strip()
            enemy_group = EnemyGroup(name, enemy1, enemy2, enemy3, enemy4, posByte, visByte)
            ENEMY_GROUPS_ARRAY.append(enemy_group)

    namesFile.close()

def printAllEnemyGroups():
    read_enemy_groups()

    print("ID | Enemy 1       | Enemy 2       | Enemy 3       | Enemy 4")
    for i, eg in enumerate(ENEMY_GROUPS_ARRAY):
        print(hex(i)[2:].rjust(2) + " | " + eg.getEnemy1c().ljust(13) + " | " + eg.getEnemy2c().ljust(13) 
              + " | " + eg.getEnemy3c().ljust(13) + " | " + eg.getEnemy4c())

def printEnemyGroup(id):
    read_enemy_groups()
    eg = ENEMY_GROUPS_ARRAY[int(id, 16)]
    print("============================================================\n " + eg.getName() + "\n============================================================")
    print("ID | Enemy 1       | Enemy 2       | Enemy 3       | Enemy 4")
    print(id.rjust(2) + " | " + eg.getEnemy1c().ljust(13) + " | " + eg.getEnemy2c().ljust(13) 
            + " | " + eg.getEnemy3c().ljust(13) + " | " + eg.getEnemy4c())

    print("\nMusic: " + eg.getMusic())
    print("\nPosition Byte: " + eg.getPositionByte())
    print("\nPalette Byte: " + eg.getPalette())

def getEnemyGroupID(identifier):
    if is_hex(identifier):
        return identifier.zfill(2)
    
    for i, eg in enumerate(ENEMY_GROUPS_ARRAY):
        if eg.isName(identifier):
            return hex(i)[2:].zfill(2)
    return "-1"

def editEnemyGroup(input_id):
    print("\nEnter 4 enemies by ID / name, separated by commas. ID of 'FF' for nothing is accepted, and implied if less than 4 entries is given. -1 is escape.\n"
          + "Add Asterisk '*' after an Enemy's Identifier to make them a Reinforcing (Call) Ally. Keep in mind the battle needs to have enemies that use Call Ally moves, otherwise they will never appear.\n"
          + "Letters after duplicate Enemies will be automatically applied.")
    raw_input = input(" >>> ")

    if raw_input == '-1':
        print("Escaped...")
        return

    raw_input = raw_input.split(',')

    if len(raw_input) > 4:
        print('Received too many number of Identifiers. Escaped...\n')
        return
    
    elif len(raw_input) < 4:
        while(len(raw_input) != 4):
            raw_input.append('ff')


    Enemy_ID_Ints = []
    Enemy_Extra_Ints = [0, 0, 0, 0] # Leftmost Bit is for isReinforcement, Remaining 7 Bits is for Letter (A, B, C, D)

    for idx_counter, identifier in enumerate(raw_input):
        identifier = identifier.strip()
        
        isReinforcement = 0
        if identifier[-1] == '*':
            isReinforcement = 0b10000000 #0x80, 0d128
            identifier = identifier[:-1]

        int_to_append = 0

        if is_hex(identifier):
            int_to_append = int(identifier, 16)
            
        else:
            enemy_id = ''

            for idx, enemy in enumerate(ENEMY_ARRAY):
                if enemy.isName(identifier):
                    enemy_id = idx

            if enemy_id == '':
                print("Invalid Entry received...")

            int_to_append = enemy_id

        
        ### ----
        Enemy_ID_Ints.append(int_to_append)

        if int_to_append != 0xff: # FF is the ID of no enemy
            # There was already 1 instance of a non-zero Enemy ID
            if Enemy_ID_Ints.count(int_to_append) == 2:
                # Add A to the 1st and B to the 2nd.
                Enemy_Extra_Ints[idx_counter] = 2 #adds B to current one
                Enemy_Extra_Ints[Enemy_ID_Ints.index(int_to_append)] += 1 #adds A to the first (and only other) index with enemy ID
            
            elif Enemy_ID_Ints.count(int_to_append) == 3:
                Enemy_Extra_Ints[idx_counter] = 3 #adds C to current one
            
            elif Enemy_ID_Ints.count(int_to_append) == 4:
                Enemy_Extra_Ints[idx_counter] = 4 #adds D to current one
            elif Enemy_ID_Ints.count(int_to_append) > 4:
                print("A severe error occured in editEnemyGroup() when trying to add letters to duped enemies.\nProgram tried to add an enemy past 4 of itself???\nEscaped bad situation...\n")
                return # Immediately Escape Error without Editing the ROM.
        
        Enemy_Extra_Ints[idx_counter] += isReinforcement #either 0 or 0x80 depending on earlier detection of an *

    if len(Enemy_ID_Ints) > 4 or len(Enemy_Extra_Ints) > 4:
        print('Received incorrect nummber of identifiers?')
        return

    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_GROUPS_OFFSET
        offset += int(input_id, 16) * ENEMY_GROUPS_LENGTH

        file.seek(offset)
        
        for i in range(4):
            file.write(Enemy_ID_Ints[i].to_bytes(1, 'big'))
            file.write(Enemy_Extra_Ints[i].to_bytes(1, 'big'))

        print("\nSuccessfully edited the Enemy Group's Enemies!\n")

def printEnemyGroupPositionTable():
    print("ID | String")
    for i, string in enumerate(ENEMY_GROUP_POSITIONS):
        print(hex(i)[2:].rjust(2) + " | " + string)

def editEnemyGroupPosition(id):
    printEnemyGroupPositionTable()
    print("\nInput a single raw Hex. -1 to Escape.\n")
    raw_input = input(" >>> ")

    if raw_input == '-1' or not is_hex(raw_input) or len(raw_input) > 1:
        print("Escaped...")
        return

    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_GROUPS_OFFSET
        offset += int(id, 16) * ENEMY_GROUPS_LENGTH
        offset += 8

        file.seek(offset)
        
        byte8 = ENEMY_GROUPS_ARRAY[int(id, 16)].getSpecials() + raw_input
        file.write(bytes.fromhex(byte8))

        print("\nSuccessfully edited the Enemy Group's Position Byte!\n")

def editSpecialEncounters(id):
    print("\nInput a single raw Hex. -1 to Escape.\n")
    raw_input = input(" >>> ")

    if raw_input == '-1' or not is_hex(raw_input) or len(raw_input) > 1:
        print("Escaped...")
        return

    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_GROUPS_OFFSET
        offset += int(id, 16) * ENEMY_GROUPS_LENGTH
        offset += 8

        file.seek(offset)
        
        byte8 = raw_input + ENEMY_GROUPS_ARRAY[int(id, 16)].getPosition()
        file.write(bytes.fromhex(byte8))

        print("\nSuccessfully edited the Enemy Group's Position Byte!\n")

def editEnemyGroupPalette(id):
    print("\nInput a single raw Hex. -1 to Escape.\n")
    raw_input = input(" >>> ")

    if raw_input == '-1' or not is_hex(raw_input) or len(raw_input) > 1:
        print("Escaped...")
        return


    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_GROUPS_OFFSET
        offset += int(id, 16) * ENEMY_GROUPS_LENGTH
        offset += 9

        file.seek(offset)
        
        byte8 = ENEMY_GROUPS_ARRAY[int(id, 16)].getMusicHex() + raw_input
        file.write(bytes.fromhex(byte8))

        print("\nSuccessfully edited the Enemy Group's Palette!\n")

def editEnemyGroupMusic(id):
    print("\n0 - Nothing         1 - 8 Melodies\n2 - Flippant Foe    3 - Dangerous Foe\n4 - Hippie         5 - Giegue\n")
    print("\nInput a single raw Hex. -1 to Escape.\n")
    raw_input = input(" >>> ")

    if raw_input == '-1' or not is_hex(raw_input) or len(raw_input) > 1:
        print("Escaped...")
        return


    with open(DIR_ROM, 'r+b') as file:
        offset = ENEMY_GROUPS_OFFSET
        offset += int(id, 16) * ENEMY_GROUPS_LENGTH
        offset += 9

        file.seek(offset)
        
        byte8 = raw_input + ENEMY_GROUPS_ARRAY[int(id, 16)].getPalette()
        file.write(bytes.fromhex(byte8))

        print("\nSuccessfully edited the Enemy Group's Music Byte!\n")

def editEnemyGroupString(id):
    new_str = input("Input new String:\n >>> ")

    with open(DIR_ENEMYGROUPNAME, "r") as file:
        data = file.readlines()
    data[int(id, 16)] = new_str + "\n"
    with open(DIR_ENEMYGROUPNAME, "w") as file:
        file.writelines(data)


### Random Encounter Groups ======================================================================================
def read_random_encounter_groups():
    read_enemy_groups()

    ENCOUNTER_TABLE_ARRAY.clear()
    with open(DIR_ROM, "rb") as file:
        file.seek(ENCOUNTER_GROUPS_OFFSET)

        for i in range(ENCOUNTER_GROUPS_COUNT):
            enemyGroupBytes = []
            # Length of 16
            for j in range(16):
                enemyGroupBytes.append(bytes.hex(file.read(1)))
            ENCOUNTER_TABLE_ARRAY.append(enemyGroupBytes)

def printAllEncounterGroups():
    read_random_encounter_groups()

    print("All Random Encounter Tables\n")
    for i, eg in enumerate(ENCOUNTER_TABLE_ARRAY):
        try:
            print(str(i).rjust(2) + " | " + ENCOUNTER_GROUPS_STRINGS[i] +
                "\n==================================================================================================================================================")
        except Exception:
            print("No String sadge")

        GroupStrings = []
        for j, g in enumerate(eg):
            # Convert Enemy Group ID into a List of 4 Strings
            try:
                GroupStrings.append(ENEMY_GROUPS_ARRAY[int(g, 16)])
            except Exception:
                GroupStrings.append(["", "", "", ""])
        
        for j in range(int(len(GroupStrings) / 2)):
            print("[" + GroupStrings[j*2].getEnemies() + "] === [" + GroupStrings[j*2+1].getEnemies() + "]")

def printEncounterGroup(id):
    read_random_encounter_groups()

    if not is_hex(id) or int(id, 16) >= len(ENCOUNTER_TABLE_ARRAY):
        print("Invalid ID received for print Encounter Group...")
        return

    GroupStrings = []
    for j, g in enumerate(ENCOUNTER_TABLE_ARRAY[int(id, 16)]):
        # Convert Enemy Group ID into a List of 4 Strings
        try:
            GroupStrings.append(ENEMY_GROUPS_ARRAY[int(g, 16)])
        except Exception:
            GroupStrings.append(["", "", "", ""])
    
    for j in range(int(len(GroupStrings) / 2)):
        print("[" + GroupStrings[j*2].getEnemies() + "] === [" + GroupStrings[j*2+1].getEnemies() + "]")

def editEncounterGroup():
    while(True):
        printAllEncounterGroups()
        input_id = input("\nEnter ID / Name of Encounter Table to edit, or -1 to escape...\n >>> ")

        if input_id == '-1':
            return

        for i in range(len(ENCOUNTER_GROUPS_STRINGS)):
            if input_id.lower() == ENCOUNTER_GROUPS_STRINGS[i].lower():
                input_id = i
                break

        try:
            input_id = int(input_id)
        except Exception:
            print("That wasn't a number...\n\n")
            continue
        
        if input_id < 0 or input_id > len(ENCOUNTER_TABLE_ARRAY):
            print("That wasn't a valid ID...\n\n")
            continue
        
        while(True):
            print(str(input_id).rjust(2) + " | " + ENCOUNTER_GROUPS_STRINGS[input_id] + "\n")
            printEncounterGroup(hex(input_id)[2:])

            print("\nEnter IDs separated by commas. ID of '0' is accepted, and implied if less than 16 entries is given. -1 is escape.\n"
                + "Less than 16 entries is fine. Entries will get multiplied out.")
            
            items = input(" >>> ")

            if items == '-1':
                print("Escaped...")
                break

            items = items.split(',')

            if len(items) > 16:
                print('Received too many entries...\n')
                continue
            elif len(items) == 1: # Length of 1
                while len(items) < 16:
                    items.append(items[0])
            elif len(items) == 2: # Length of 2
                while len(items) < 16:
                    items.append(items[0])
                    items.append(items[1])
            elif len(items) <= 4: # Length of <4
                while len(items) < 4:
                    items.append('00')

                while len(items) < 16:
                    items.append(items[0])
                    items.append(items[1])
                    items.append(items[2])
                    items.append(items[3])
            elif len(items) <= 8: #Length of <8
                while len(items) < 8:
                    items.append('00')

                temp = items.copy()
                for it in items:
                    temp.append(it)
                items = temp.copy()
            else: # Length of <16
                while len(items) < 16:
                    items.append('00')

            BytesToWrite = ''
            for item in items:
                item = item.strip()
                
                item = getEnemyGroupID(item)
                
                if item == "-1":
                    print("Invalid Entry received...")
                    return
                BytesToWrite += item

                #if is_hex(item):
                #    BytesToWrite += item.zfill(2)
                
                #else:
                #    print("Invalid Entry received...")
                #    return

            if len(BytesToWrite) != 32:
                print('Received incorrect nummber of identifiers?')
                continue

            with open(DIR_ROM, 'r+b') as file:
                offset = ENCOUNTER_GROUPS_OFFSET
                offset += input_id * ENCOUNTER_GROUPS_LENGTH

                file.seek(offset)

                file.write(bytes.fromhex(BytesToWrite))
                print("\nSuccessfully edited the Encounter Table!\n")

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #

##################################################################################################################
### Main Code ------------------------------------------------------------------------------------------------ ###
##################################################################################################################
ContProgram = True
while(ContProgram):
    read_items()

    print('======================================================================')
    print('======================================================================')
    print('======================================================================')
    print("\n###-----------COMMAND-------------###\n0 - Item Viewer/Editor\n1 - PSI Viewer/Editor\n2 - Enemy Viewer/Editor\n3 - Encounter Groups Editor\n4 - Shop Editor\n5 - Objects Editor\n6 - Character Stats Editor\ne - End Program\n")
    Command = input("Enter a Command: ")
    print('\n')
    if Command.lower() == 'exit' or Command.lower() == 'e':
        break

    # Item Viewer and Editor
    if Command == "0" or Command.lower() == "item":
    #-------------------------------------------------------------------------------------
        read_items()
    #-------------------------------------------------------------------------------------
        while(True):
            print('======================================================================')
            print('======================================================================')
            print('======================================================================')
            print('\n###-------Item Viewer/Editor-------###')
            print("0 or printall - Print all Items (Hex)\nXX - View Item (by ID)\nstring - View Item (by name)\ne - Exit\n")
            Command = input('Enter a Command: ')

            if Command == '0' or Command.lower() == 'printall':
                printAllItems()
            elif Command.lower() == 'exit' or Command.lower() == 'e':
                break
            else:
                current_ID = getItemID(Command)
                if current_ID != '-1':
                    while(True):
                        printItem(current_ID)
                        print('###--------- View and Edit ---------###')
                        print('\n0/e - Exit\n1 - Change Price\n2 - Edit Item Stats\n3 - Edit Item Flags\n4 - Edit Item Actions\n5 - Update Item\'s Description Pointer\n')
                        Command = input('Enter a Command: ')
                        
                        if Command == '0' or Command.lower() == 'e':
                            break
                        elif Command == '1':
                            editItemPrice(current_ID)
                        elif Command == '2':
                            editItemStats(current_ID)
                        elif Command == '3':
                            editItemFlags(current_ID)
                        elif Command == '4':
                            editItemActions(current_ID)
                        elif Command == '5':
                            editItemDescriptionPtr(current_ID)

    elif Command == "1" or Command.lower() == "psi":
    #-------------------------------------------------------------------------------------
        read_psi()
    #-------------------------------------------------------------------------------------
        while(True):
            print('======================================================================')
            print('======================================================================')
            print('======================================================================')
            print('\n###------- PSI Viewer/Editor -------###')
            print('\n0 or printall - Print all PSI\nXX - View PSI (by ID)\nstring - View PSI (by name)\ne - Exit\n')
            Command = input('Enter a Command: ')

            if Command == '0' or Command.lower() == 'printall':
                printAllPSI()
            elif Command.lower() == 'exit' or Command.lower() == 'e':
                break
            else:
                current_PSI_ID = getPSI_ID(Command)

                if current_PSI_ID != '-1':
                    while(True):
                        printPSI(current_PSI_ID)
                        print('###--------- View and Edit ---------###')
                        print('\n0/e - Exit\n1 - Change Ninten\'s Level Learned\n2 - Change Ana\'s Level Learned\n3 - Change PP Cost\n4 - Change Actions\n')
                        Command = input('Enter a Command: ')
                        
                        if Command == '0' or Command.lower() == 'e':
                            break
                        elif Command == '1' or Command == '2':
                            changePSILevel(current_PSI_ID, int(Command))
                        elif Command == '3':
                            editPSICost(current_PSI_ID)
                        elif Command == '4':
                            editPSIAction(current_PSI_ID)
                
    
    elif Command == '2' or Command.lower() == 'enemy':
        read_enemies()
        while(True):
            print('======================================================================')
            print('======================================================================')
            print('======================================================================')
            print('\n###------ Enemy Viewer/Editor ------###')
            print('\nA - printAll Enemies (by ID)\nAA - printAll Enemies (by Area)\nMP - printAll Enemies (by MP Area)'
                + '\nMP1 - printAll Enemies Resistances'
                + '\nAtt - Print All Enemy Attacks\ndump - Dump All\nfull - Full Dump All Enemies'
                + '\nXX - View Enemy (by ID)\nstring - View Enemy (by name)\ne - Exit\n')
            Command = input('Enter a Command: ')
            
            if Command == 'A':
                printAllEnemies()
            elif Command == 'AA':
                printAllEnemiesByArea("Enemy Areas.txt", 0)
            elif Command.lower() == 'mp':
                printAllEnemiesByArea("MP Areas.txt", 0)
            elif Command.lower() == "mp1":
                printAllEnemiesByArea("MP Areas.txt", 1)
            elif Command.lower() == 'exit' or Command.lower() == 'e':
                break
            elif Command == 'Att':
                printAllEnemiesAttacks()
            elif Command == 'dump':
                dumpAllEnemies()
            elif Command == "full":
                fulldumpAllEnemies("VanillaAreas.txt")
            else:
                current_ID = getEnemyID(Command)

                if current_ID != '-1':
                    while(True):
                        printEnemy(current_ID)
                        print('###--------- View and Edit ---------###')
                        print('\n0/e - Exit\n1 - Edit Attacks\n2 - Edit Dropped Item\n3 - Edit Flags\n4 - Edit Core Stats\n5 - Edit Exp/Money\nhp, pp, off, def - Edit Stat')
                        Command = input('Enter a Command: ')
                        
                        if Command.lower() == '0' or Command.lower() == 'e':
                            break
                        elif Command == '1':
                            editBattle(current_ID)
                        elif Command == '2':
                            editEnemyDrop(current_ID)
                        elif Command == '3':
                            editEnemyFlags(current_ID)
                        elif Command.lower() == 'hp' or Command.lower() == 'pp' or Command.lower() == 'off' or Command.lower() == 'def':
                            editEnemyStat(current_ID, Command.lower())
                        elif Command == '4':
                            editEnemyCore(current_ID)
                        elif Command == '5':
                            editEnemyTwoBytes(current_ID)

    elif Command == '3':
        while(True):
            print('======================================================================')
            print('\n###------ Encounter Groups ------###')
            print('\n0 - View/Edit Enemy Groups\n1 - Print Random Encounter Table\ne - Exit\n')
            
            Command = input('Enter a Command: ')

            if Command.lower() == 'e':
                break
            elif Command == '0':
                while(True):
                    printAllEnemyGroups()
                    print('###--------- View and Edit ---------###')
                    print("\n-1 - Escape\nID - View and Edit Enemy Group")
                    Command = input("Enter a Command: ")

                    if Command.lower() == '-1':
                        break

                    if not is_hex(Command):
                        print("That wasn't a number...\n\n")
                        continue
                    
                    if int(Command, 16) < 0 or int(Command, 16) > len(ENEMY_GROUPS_ARRAY):
                        print("That wasn't a valid ID...\n\n")
                        continue

                    current_ID = Command
                    while(True):
                        printEnemyGroup(current_ID)
                        print("Now Editing " + current_ID + ": " + ENEMY_GROUPS_ARRAY[int(current_ID, 16)].getEnemies() + "\n")

                        print("e - Escape\n1 - Edit Enemies\n2 - Set Positioning\n3 - Set String\n4 - Change Palette\n5 - Change Music\n9 - Edit Special Encounters")
                        Command = input("Enter Command: ")

                        if Command.lower() == 'e':
                            break
                        
                        if Command == '1':
                            editEnemyGroup(current_ID)
                        elif Command == '2':
                            editEnemyGroupPosition(current_ID)
                        elif Command == '3':
                            editEnemyGroupString(current_ID)
                        elif Command == '4':
                            editEnemyGroupPalette(current_ID)
                        elif Command == '5':
                            editEnemyGroupMusic(current_ID)
                        elif Command == '9':
                            editSpecialEncounters(current_ID)

            elif Command == '1':
                editEncounterGroup()

    elif Command == '6' or Command.lower == 'stats':
        while(True):
            print('======================================================================')
            print('======================================================================')
            print('======================================================================')
            print('\n###------ Character Viewer/Editor ------###')
            print('\n0 - Print all Characters\n1~5 - View/Edit Specific Character\ne - Exit\n')
            
            Command = input('Enter a Command: ')

            if Command.lower() == 'e':
                break
            elif Command == '0':
                printAllCharas()
            elif Command == '1' or Command == '2' or Command == '3' or Command == '4' or Command == '5':
                chara_id = int(Command)
                name = 'Ninten'
                if chara_id == 2:
                    name = 'Ana'
                elif chara_id == 3:
                    name = 'Lloyd'
                elif chara_id == 4:
                    name = 'Teddy'
                elif chara_id == 5:
                    name = 'Pippi'

                while(True):
                    print('======================================================================')
                    print('======================================================================')
                    print('======================================================================')
                    print('Viewing Character ' + name)
                    printChara(chara_id)

                    print('\n###-----------COMMAND-------------###\ne - Exit\n0 - Edit All\n1 - Edit Fight\n2 - Edit Speed\n3 - Edit Wisdom\n4 - Edit Strength\n5 - Edit Force\n')
                    Command = input("Enter a Command: ")
                    
                    if Command.lower() == 'e':
                        break
                    elif Command == '0':
                        print('g - by Growth values\na - by Average\n(nothing) - by Raw Value (only works with no RNG mod)\n')
                        input_method = input(' >>> ').lower()

                        if not (input_method == 'g' or input_method == 'a' or input_method == ''):
                            print('Invalid input type...')
                            break
                        editCharaStat(chara_id, 1, input_method)
                        editCharaStat(chara_id, 2, input_method)
                        editCharaStat(chara_id, 3, input_method)
                        editCharaStat(chara_id, 4, input_method)
                        editCharaStat(chara_id, 5, input_method)
                    elif Command == '1' or Command == '2' or Command == '3' or Command == '4' or Command == '5':
                        print('g - by Growth values\na - by Average\n(nothing) - by Raw Value (only works with no RNG mod)\n')
                        input_method = input(' >>> ').lower()

                        if not (input_method == 'g' or input_method == 'a' or input_method == ''):
                            print('Invalid input type...')
                            break
                        editCharaStat(chara_id, int(Command), input_method)
        
    elif Command == '4':
        editShops()

    elif Command == '5':
        while(True):
            print('======================================================================')
            print('\n###------ Objects / Presents Editor ------###')
            print('\n0 - View/Edit Objects\n1 - View/Edit Presents\ne - Exit\n')
            
            Command = input('Enter a Command: ')

            if Command.lower() == 'e':
                break
            
            if Command == '0':
                editObjects()
            if Command == '1':
                editPresents()