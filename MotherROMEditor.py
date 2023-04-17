import os
#import Translator.ThingyTableTranslate

### EDITABLES ###
rom_name = "Mother Prime.nes"
strings_folder = 'strings'

item_name_dir = strings_folder + "/ItemNames.txt"
psi_name_dir = strings_folder + "/PSINames.txt"
enemy_name_dir = strings_folder + "/EnemyNames.txt"
battle_name_dir = strings_folder + "/BattleNames.txt"

### CONSTANTS ###
script_dir = os.path.dirname(__file__)
ROM_DIR = script_dir + '/' + rom_name

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
    def __init__(self, id, name, pp, ninten, ana):
        self.ID = id
        self.PP = pp
        self.ninten = ninten
        self.ana = ana
        self.name = name

    def getID(self):
        if self.ID == '':
            return '0'
        return self.ID
    def getPP(self):
        return self.PP

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

class Enemy():
    def __init__(self, id, flags, hp, pp, offense, defense, core, attacks, exp, cash, item, name):
        self.id = id
        self.flags = flags
        self.exp = exp
        self.money = cash
        self.item = item
        self.name = name

        self.Core = core
        self.attacks = attacks

        # Complex Data
        self.hp = ''
        self.pp = ''
        self.Off = ''
        self.Def = ''

        self.death = ''
        self.type = ''

        self.HP_CONST = ''
        self.PP_CONST = ''
        self.OFF_CONST = ''
        self.DEF_CONST = ''

        # reverse order bytes
        low_hp = ''
        low_pp = ''
        low_off = ''
        low_def = ''

        # Bits processing

        hpBits = getBits2(hp)
        ppBits = getBits2(pp)
        offBits = getBits2(offense)
        defBits = getBits2(defense)

        for i in range(16):
            # first 8 bits - low value
            if i < 8:
                low_hp += hpBits[i]
                low_pp += ppBits[i]
                low_off += offBits[i]
                low_def += defBits[i]

            # last 2 bits - high value
            elif i >= 14: #14, 15
                self.hp += hpBits[i]
                self.pp += ppBits[i]
                self.Off += offBits[i]
                self.Def += defBits[i]

            # 3 bits - off, def, death and typee
            elif i >= 11: #11, 12, 13
                self.death += offBits[i]
                self.type += defBits[i]

                self.HP_CONST += hpBits[i]
                self.PP_CONST += ppBits[i]
            
            # bits 8, 9, - constants
            else:
                self.OFF_CONST += offBits[i]
                self.DEF_CONST += defBits[i]
                self.HP_CONST += hpBits[i]
                self.PP_CONST += ppBits[i]
            
        self.hp += low_hp
        self.pp += low_pp
        self.Off += low_off
        self.Def += low_def

    def getID(self):
        return self.id
    def getName(self):
        return self.name
    def isName(self, str):
        return self.name.lower() == str.lower()
    def getItem(self):
        return getItemName(self.item)
    
    def getOffenseByte(self):
        return self.Off + self.death + self.OFF_CONST
    def getDefenseByte(self):
        return self.Def + self.type + self.DEF_CONST
    
    def getHP(self):
        return int(self.hp, 2)
    def getPP(self):
        return int(self.pp, 2)
    def getOff(self):
        return int(self.Off, 2)
    def getDef(self):
        return int(self.Def, 2)

    def getDeathID(self):
        return self.death
    def getTypeID(self):
        return self.type

    def get_HP_CONST(self):
        return self.HP_CONST
    def get_PP_CONST(self):
        return self.PP_CONST
    def get_OFF_CONST(self):
        return self.OFF_CONST
    def get_DEF_CONST(self):
        return self.DEF_CONST

    def getCores(self):
        output = []
        for stat in self.Core:
            output.append(int(stat, 16))

        return output
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

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #
### Functions ###

# Returns Number
def getBit(hex, bit):
    return int(bin(int(hex, 16))[2:].zfill(8)[bit])
    
# Returns a List of Numbers
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

def getBits2(hex):
    if hex == '0000':
        return '0000000000000000'
    
    string = bin(int(hex, 16))[2:].zfill(16)
    
    string.lstrip('0b')
    return string

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

# ========================================================================================================================= #
### ===================================================================================================================== ###
# ========================================================================================================================= #

#####################################################################################################
### Item Reader --------------------------------------------------------------------------------- ###
#####################################################################################################

def read_items():
    ITEMS_ARRAY.clear()
    namesFile = open(script_dir + '/' + item_name_dir, 'r')

    with open(ROM_DIR, 'rb') as file:
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

#####################################################################################################
### Item Printer -------------------------------------------------------------------------------- ###
#####################################################################################################

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

#####################################################################################################
### Item Editor -------------------------------------------------------------------------------- ###
#####################################################################################################

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
    with open(ROM_DIR, 'r+b') as file:
        offset = ITEM_POS

        offset += int(id, 16) * 8
        offset += 6

        file.seek(offset)

        file.write(bytes.fromhex(BytesToWrite))

        print('\n ===> Successfully edited price!\n')
    
    read_items()
    return


# Item Stats Editor

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
    with open(ROM_DIR, 'r+b') as file:
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
        with open(ROM_DIR, 'r+b') as file:
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
        with open(ROM_DIR, 'r+b') as file:
            offset = ITEM_POS

            offset += int(id, 16) * 8
            offset += 4 + ActionType

            file.seek(offset)

            file.write(bytes.fromhex(Byte))

            print('\n ===> Successfully edited item\'s action!\n')
        
        read_items()
        return

#####################################################################################################
### Item Description Ptr Editor! ---------------------------------------------------------------- ###
#####################################################################################################

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
    with open(ROM_DIR, 'r+b') as file:
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
### PSI Reader ---------------------------------------------------------------------------------- ###
#####################################################################################################

def read_psi():
    PSI_ARRAY.clear()
    namesFile = open(script_dir + '/' + psi_name_dir, 'r')

    with open(ROM_DIR, 'rb') as file:
        file.seek(PSI_POS)

        for i in range(0, 63):
            # Bytes 0, 1 - NamePtr
            Name = bytes.hex(file.read(2))
            
            # 2, 3 - Ninten, Ana Level
            NintenLevel = bytes.hex(file.read(1))
            AnaLevel = bytes.hex(file.read(1))

            # 4, 5 - Overworld, Battle Action (not important to save)
            Overworld = bytes.hex(file.read(1))
            Battle = bytes.hex(file.read(1))

            # 6 (not really used)
            useless = bytes.hex(file.read(1))
            
            # 7 - PP Cost
            PP = bytes.hex(file.read(1))

            ### GET PSI NAMES ###
            Name = namesFile.readline().strip()

            ### Process PSI information.
            psi = PSI(hex(i).lstrip('0x'), Name, int(PP, 16), int(NintenLevel, 16), int(AnaLevel, 16))
            PSI_ARRAY.append(psi)
    
    namesFile.close()

#####################################################################################################
### PSI Printer --------------------------------------------------------------------------------- ###
#####################################################################################################

def printAllPSI():
    print('===========================================')
    print('================= ALL PSI =================')
    print('===========================================')

    # ID, Name, Ninten Level, Ana Level
    for psi in PSI_ARRAY:
        psiPrint = "--------------------\n" + psi.getID() + ' | '
        
        if psi.getName() != '':
            psiPrint += psi.getName().ljust(11) + ' | PP: ' + (str)(psi.getPP()) + '\n\n      Ninten | ' + psi.getNintenStr() + '\n         Ana | ' + psi.getAnaStr()
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
    print(psi.getName().ljust(11) + ' | PP: ' + (str)(psi.getPP()) + '\nNinten Level | ' + psi.getNintenStr() + '\n   Ana Level | ' + psi.getAnaStr())
    print('\n==============================\n')

#####################################################################################################
### PSI Level Editor ---------------------------------------------------------------------------- ###
#####################################################################################################

def changePSILevel(id, who):
    with open(ROM_DIR, 'r+b') as file:
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
    with open(ROM_DIR, 'r+b') as file:
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


    with open(ROM_DIR, 'r+b') as file:
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
### Enemies ---------------------------------------------------------------------------- ###
#####################################################################################################

#####################################################################################################
### Enemies Reader ---------------------------------------------------------------------------- ###
#####################################################################################################

def read_enemies():
    ENEMY_ARRAY.clear()
    namesFile = open(script_dir + '/' + enemy_name_dir, 'r')

    with open(ROM_DIR, 'rb') as file:
        file.seek(ENEMY_POS)

        # Entries go from 00 to FF? (only 122 used)
        for i in range(0, 122):
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
            for j in range(5):
                Cores.append(bytes.hex(file.read(1)))

            # 16 ~ 23 - Attacks
            Attacks = []
            for j in range(8):
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
            enemy = Enemy(hex(i).lstrip('0x'), Flags, HP, PP, Off, Def, Cores, Attacks, EXP, Cash, ITEM, Name)
            ENEMY_ARRAY.append(enemy)
    
    namesFile.close()
    read_battle()

def read_battle():
    BATTLE_ARRAY.clear()
    with open(script_dir + '/' + battle_name_dir, 'r') as file:
        for i in range(134):
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

#####################################################################################################
### Enemies Printer ---------------------------------------------------------------------------- ###
#####################################################################################################

def printAllEnemies():
    print('===========================================')
    print('=============== ALL ENEMIES ===============')
    print('===========================================')

    # ID |          Name | Type | HP | Off | Def 
    print('ID | Name         | Type     |  HP | Off | Def | Item')

    for enemy in ENEMY_ARRAY:
        enemyPrint = enemy.getID().rjust(2) + ' | '
        
        if enemy.getName() != '':
            enemyPrint += enemy.getName().ljust(12) + ' | ' + '   empty' + ' |'
            enemyPrint += (str)(enemy.getHP()).rjust(4) + ' |' + (str)(enemy.getOff()).rjust(4) + ' |' + (str)(enemy.getDef()).rjust(4) + ' |' + enemy.getItem().rjust(11)
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
    print(enemy.getName().ljust(13) + '\nHP: ' + str(enemy.getHP()) + '\nPP: ' + str(enemy.getPP()) + '\nOff: ' + str(enemy.getOff()) + '\nDef: ' + str(enemy.getDef()))
    cores = enemy.getCores()
    print('Fight: ' + str(cores[0]) + '\nSpeed: ' + str(cores[1]) + '\nWisdom: ' + str(cores[2]) + '\nStrength: ' + str(cores[3]) + '\nForce: ' + str(cores[4]))
    print('Dropped Item: ' + enemy.getItem())

    print('================\nFlags:\n')
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

#####################################################################################################
### Enemy Editor ---------------------------------------------------------------------------- ###
#####################################################################################################

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
    with open(ROM_DIR, 'r+b') as file:
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
    with open(ROM_DIR, 'r+b') as file:
        offset = ENEMY_POS

        offset += int(id, 16) * 32
        offset += 30

        file.seek(offset)

        file.write(bytes.fromhex(ItemID))

        print('\n ===> Successfully edited item!')
    
    read_enemies()

def editEnemyStat(id, what):
    stat = ''
    junk = ''
    stat_offset = ''

    if what == 'hp':
        stat = 'HP'
        junk = ENEMY_ARRAY[int(id, 16)].get_HP_CONST()
        stat_offset = 3
    elif what == 'pp':
        stat = 'PP'
        junk = ENEMY_ARRAY[int(id, 16)].get_PP_CONST()
        stat_offset = 5
    elif what == 'off':
        stat = 'Offense'
        Temp_Enemy = ENEMY_ARRAY[int(id, 16)]
        junk = Temp_Enemy.get_OFF_CONST() + Temp_Enemy.getDeath()
        stat_offset = 7
    elif what == 'def':
        stat = 'Defense'
        Temp_Enemy = ENEMY_ARRAY[int(id, 16)]
        junk = Temp_Enemy.get_DEF_CONST() + Temp_Enemy.getType()
        stat_offset = 9
    

    print('\nEnter in new value for ' + stat + ' (as an integer).\nYou can also input -1 to escape.\n')
    Input = ''
    try:
        Input = int(input('  >>> '))
    except ValueError:
        print(' That wasn\'t a number... Did nothing.')
        return

    if Input == -1:
        print(' <-- Escaped...')
        return
    elif Input < 0:
        print(' The value cannot be negative, silly.')
        return
    elif Input > 1023:
        print(' That value is too large. The input can\'t be larger than 10 bits (1023 in decimal).')

    # Translate the int into Bits
    raw_bits = bin(Input).lstrip('0b')
    raw_bits = raw_bits.zfill(10)

    # Move the raw bits around and make the final string
    # Low Portion x8, Junk Data x6, High Portion x2
    low = raw_bits[2:]
    high = raw_bits[:2]

    BytesToWrite = low + junk + high

    # Find the offset.
    with open(ROM_DIR, 'r+b') as file:
        offset = ENEMY_POS

        offset += int(id, 16) * 32
        offset += stat_offset

        file.seek(offset)

        file.write(int.to_bytes(int(BytesToWrite, 2), 2, 'little'))

        print('\n ===> Successfully edited ' + stat + '!\n')
    
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
    with open(ROM_DIR, 'r+b') as file:
        offset = ENEMY_POS

        offset += int(id, 16) * 32
        offset += 2

        file.seek(offset)

        file.write(Input.to_bytes(1, 'big'))

        print('\n ===> Successfully edited flags!')
    
    read_enemies()

#####################################################################################################
### Chara Editor ---------------------------------------------------------------------------- ###
#####################################################################################################
def read_charas():
    PLAYER_ARRAY.clear()

    with open(ROM_DIR, 'rb') as file:
        file.seek(GROWTH_POS)

        # Entries go from 00 to FF? (only 122 used)
        for i in range(5):
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
    return (int)(2*avg - 1)

def editCharaStat(chara_id, stat_id):
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
    
    print('g - by Growth values\na - by Average\n')
    input_method = input(' >>> ').lower()

    if not (input_method == 'g' or input_method == 'a'):
        print('Invalid input type...')
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
    if input_stat < 0 or input_stat > 255:
        print("Received a value that isn't within a byte...")
        return

    with open(ROM_DIR, 'r+b') as file:
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

    print('Enter the value for ' + stat_name + '. You can also type "-1" to make it default based on growth stats.')
    input_stat = input(' >>> ')

    try:
        input_stat = int(input_stat)
    except ValueError:
        print("Didn't receive a number as the stat value...")
        return

    if input_stat == -1:
        input_stat = int(PLAYER_ARRAY[chara_id - 1][stat_id - 1], 16) + 1
    
    with open(ROM_DIR, 'r+b') as file:
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
### Shop Editor ---------------------------------------------------------------------------- ###
#####################################################################################################

def printAllShops():
    i = 0
    print('ID | Shop Name        | Items')
    with open(ROM_DIR, 'rb') as file:
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

        with open(ROM_DIR, 'r+b') as file:
            file.seek(SHOPS_ARRAY[input_id][1])

            file.write(bytes.fromhex(BytesToWrite))

            print("\nSuccessfully edited the shop!\n")

def printAllObjects():
    i = 0
    print('ID | Object           | Item')
    with open(ROM_DIR, 'rb') as file:
        for name, offset in ITEM_OBJECTS_ARRAY:
            file.seek(offset)
            item_id = bytes.hex(file.read(1))
            

            print(str(i).rjust(2) + ' | ' + name.ljust(17) + '| ' + getItemName(item_id).rjust(11))

            if(i == 1 or i == 2):
                print("")


            i += 1

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

        with open(ROM_DIR, 'r+b') as file:
            file.seek(ITEM_OBJECTS_ARRAY[input_id][1])

            file.write(bytes.fromhex(BytesToWrite))

            print("\nSuccessfully edited the object!\n")

### Main Code ------------------------------------------------------------------------------------------------ ###
ContProgram = True
while(ContProgram):
    read_items()

    print('======================================================================')
    print('======================================================================')
    print('======================================================================')
    print("\n###-----------COMMAND-------------###\n0 - Item Viewer/Editor\n1 - PSI Viewer/Editor\n2 - Enemy Viewer/Editor\n3 - Character Stats Editor\n4 - Shop Editor\n5 - Objects Editor\ne - End Program\n")
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
                        print('\n0/e - Exit\n1 - Change Ninten\'s Level Learned\n2 - Change Ana\'s Level Learned\n3 - Change PP Cost\n')
                        Command = input('Enter a Command: ')
                        
                        if Command == '0' or Command.lower() == 'e':
                            break
                        elif Command == '1' or Command == '2':
                            changePSILevel(current_PSI_ID, int(Command))
                        elif Command == '3':
                            editPSICost(current_PSI_ID)
                
    
    elif Command == '2' or Command.lower() == 'enemy':
        read_enemies()
        while(True):
            print('======================================================================')
            print('======================================================================')
            print('======================================================================')
            print('\n###------ Enemy Viewer/Editor ------###')
            print('\n0 or printall - Print all Enemies\nXX - View Enemy (by ID)\nstring - View Enemy (by name)\ne - Exit\n')
            Command = input('Enter a Command: ')
            
            if Command == '0' or Command.lower() == 'printall':
                printAllEnemies()
            elif Command.lower() == 'exit' or Command.lower() == 'e':
                break
            else:
                current_ID = getEnemyID(Command)

                if current_ID != '-1':
                    while(True):
                        printEnemy(current_ID)
                        print('###--------- View and Edit ---------###')
                        print('\n0/e - Exit\n1 - Edit Attacks\n2 - Edit Dropped Item\n3 - Edit Flags\nhp, pp, off, def - Edit Stat')
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


    elif Command == '3' or Command.lower == 'stats':
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
                        editCharaStat(chara_id, 1)
                        editCharaStat(chara_id, 2)
                        editCharaStat(chara_id, 3)
                        editCharaStat(chara_id, 4)
                        editCharaStat(chara_id, 5)
                    elif Command == '1' or Command == '2' or Command == '3' or Command == '4' or Command == '5':
                        editCharaStat(chara_id, int(Command))
        
    elif Command == '4':
        editShops()

    elif Command == '5':
        editObjects()