import os

### PATHS ###
script_dir = os.path.dirname(__file__)

rom_dir = script_dir + "/Mother Prime.nes"
item_description_dir = script_dir + "/Translator/Item Descriptions.txt"
enemy_discription_dir = script_dir + "/Translator/Enemy Descriptions.txt"


item_name_dir = script_dir + "/Translator/Item Names.txt"
teleport_name_dir = script_dir + "/Translator/Place Names.txt"
psi_name_dir = script_dir + "/Translator/PSI Names.txt"
status_name_dir = script_dir + '/Translator/Status Names.txt'
enemy_name_dir = script_dir + "/Translator/Enemy Names.txt"


### CONSTANTS ###

ITEM_POS = 0x01810

TELEPORT_POS = 0x01C10
PSI_POS = 0x01E10

ENEMY_POS = 0x2c010
ENEMY_NAME_PTR_OFFSET = 0x18 #2 bytes, 18 and 19, by little

NAME_PTR_LENGTH = 2

ENEMY_DESC_POS = 0x30f4c
DESC_PTR_LENGTH = 3

ITEM_DESC_POS = 0x30bc8

STATUS_OFFSETS = {"Uncon." : "608", "Petrified" : "610", "Paralyzed" : "616", "Asleep" : "61D",
                  "Confused" : "624", "Puzzled" : "62B", "Poison" : "632", "Cold" : "63B"}


STATUS_PTR_LOCATIONS = {"Uncon." : 0x3c63c, "Petrified" : "610", "Paralyzed" : "616", "Asleep" : "61D",
                  "Confused" : "624", "Puzzled" : "62B", "Poison" : "632", "Cold" : "63B"}

PSI_NAME_OFFSET = 0xa10 #0x42e
ENEMY_NAME_OFFSET = 0x641

ITEM_COUNT = int('7f', 16)
PLACE_COUNT = 40
PSI_COUNT = 63
ENEMY_COUNT = 122

### GLOBALS ###

hex_table = []
string_table = []

def initialize_thingy_table():
    tableFile = open(script_dir + "/Translator/ThingyTable.txt", "r")
    for line in tableFile:
        line = line.split('=')
        hexval = line[0].strip()

        if hexval == 'A0':
            strval = ' '
        else:
            strval = line[1].strip()
        
        if len(strval) > 1:
            strval = strval.lower()

        hex_table.append(hexval)
        string_table.append(strval)
    tableFile.close()

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def translateChar(char):
    for i in range(0, len(string_table)):
        if char == string_table[i]:
            return hex_table[i]
    return "-1"

def translate(string):
    output = ""
    temp = ''
    toggle = False
    toggle_quotes = False

    for c in string:
        if toggle:
            temp += c

            if translateChar(temp.lower()) != '-1':
                output += translateChar(temp.lower()) + ' '
                temp = ''
                toggle = False

        elif c == '\\' or c == '<' or c == '[':
            toggle = True
            temp += c
        elif c == '\n':
            temp += '01' + " "
        elif c == '"':
            if toggle_quotes:
                toggle_quotes = False
                output += translateChar('"2') + ' '
            else:
                toggle_quotes = True
                output += translateChar('"1') + ' '
        else:
            output += translateChar(c) + " "

    return output

#####################################################################################################
### Item Descriptions --------------------------------------------------------------------------- ###
#####################################################################################################

def readDescriptions(description_dir):
    DESCRIPTION_ARRAY = {}

    with open(description_dir, 'r') as file:
        string = ''
        id = ''
        OFFSET = '' # The Offset is Read from the File's first line

        for line in file:
            line = line.split("#")[0]

            if len(line) > 2 and line[:2] == '0x':
                OFFSET = line[2:]

            # Found new Item ID, process old, begin new description.
            elif len(line.strip()) == 2 and is_hex(line[0:2].strip()):
                if id != '':
                    DESCRIPTION_ARRAY[id] = string[:-3] + ' 00'

                    string = ''
                    id = ''

                id = line[0:2].strip()
            
            # Continue writing current description.
            elif id != '':
                string += translate(line) + '01 '

        return OFFSET, DESCRIPTION_ARRAY
# Returns a 3 byte Pointer
def calcDescriptionPointer(description_offset):
    return int.to_bytes(description_offset - int('60010', 16), DESC_PTR_LENGTH, 'little')

def writeDescriptions(description_dir, pointers_offset):
    OFFSET, DESCRIPTION_ARRAY = readDescriptions(description_dir)
    POINTERS_ARRAY = []

    with open(rom_dir, 'r+b') as file:
        file.seek(int(OFFSET, 16))
        
        for i in range(ITEM_COUNT):
            hexID = hex(i)[2:].zfill(2)

            bytesString = DESCRIPTION_ARRAY.get(hexID.upper(), '-1')

            if bytesString == '-1':
                POINTERS_ARRAY.append(int.to_bytes(0, DESC_PTR_LENGTH, 'little'))

            else:
                POINTERS_ARRAY.append(calcDescriptionPointer(file.tell()))
                file.write(bytes.fromhex(bytesString))
    
        file.seek(pointers_offset)
        for byte in POINTERS_ARRAY:
            file.write(byte)

        #############################################
        print("Updated all Item descriptions...")

#####################################################################################################
### All Names --------------------------------------------------------------------------- ###
#####################################################################################################

# Translates real location of String (starts at 0) to a Pointer.
# Returns a 2 byte Pointer
def calcNamePointer(name_offset):
    return int.to_bytes(name_offset + int('7ff0', 16), NAME_PTR_LENGTH, 'little')

ITEM_NAME_ARRAY = []
PLACE_NAME_ARRAY = []
PSI_NAME_ARRAY = []
ENEMY_NAME_ARRAY = []

def readAllNames():
    with open(item_name_dir, 'r') as file:
        for line in file:
            ITEM_NAME_ARRAY.append(translate(line.strip()) + '00')
    with open(teleport_name_dir, 'r') as file:
        for line in file:
            PLACE_NAME_ARRAY.append(translate(line.strip()) + '00')
    with open(psi_name_dir, 'r') as file:
        for line in file:
            PSI_NAME_ARRAY.append(translate(line.strip()) + '00')
    with open(enemy_name_dir, 'r') as file:
        for line in file:
            ENEMY_NAME_ARRAY.append(translate(line.strip()) + '00')

def writeItemNames():
    ITEM_POINTERS_ARRAY = []
    with open(rom_dir, 'r+b') as file:
        # WRITE ITEM STRINGS & record pointers

        file.seek(int('11', 16))
        for i in range(int('7f', 16)):
            
            bytesString = ITEM_NAME_ARRAY[i]
            if bytesString == '':
                ITEM_POINTERS_ARRAY.append('-1')

            else:
                ITEM_POINTERS_ARRAY.append(calcNamePointer(file.tell()))
                
                file.write(bytes.fromhex(bytesString))

# A function to edit all Names.
# The order is: Item, Location, PSI, Status, Enemies
def writeAllNames():
    readAllNames()

    ITEM_POINTERS_ARRAY = []
    PLACE_POINTERS_ARRAY = []
    PSI_POINTERS_ARRAY = []
    ENEMY_POINTERS_ARRAY = []

    with open(rom_dir, 'r+b') as file:
    #############################################
    ### WRITE ITEM STRINGS & record pointers
    #############################################
        file.seek(int('11', 16))
        for i in range(ITEM_COUNT):
            bytesString = ITEM_NAME_ARRAY[i]
            if bytesString == '':
                ITEM_POINTERS_ARRAY.append('-1')

            else:
                ITEM_POINTERS_ARRAY.append(calcNamePointer(file.tell()))
                
                file.write(bytes.fromhex(bytesString))
    
    #############################################
    # WRITE TELEPORT / TRAIN STRINGS & record pointers
    #############################################    
        # we like a dictionary to write in duped town names for the train stations
        PlacePointers_Dictionary = {}
        for i in range(PLACE_COUNT):
            bytesString = ''
            
            if len(PLACE_NAME_ARRAY) > i:
                bytesString = PLACE_NAME_ARRAY[i]

            if bytesString == '':
                PLACE_POINTERS_ARRAY.append('-1')

            elif PlacePointers_Dictionary.get(bytesString) != None:
                namePtr = PlacePointers_Dictionary[bytesString]
                PLACE_POINTERS_ARRAY.append(namePtr)

            else:
                namePtr = calcNamePointer(file.tell())
                PLACE_POINTERS_ARRAY.append(namePtr)
                
                file.write(bytes.fromhex(bytesString))
                PlacePointers_Dictionary[bytesString] = namePtr
        
    
    #############################################
    # WRITE PSI STRINGS & record pointers
    #############################################
        # Skip over the junk item names...
        file.seek(PSI_NAME_OFFSET)
        for i in range(len(PSI_NAME_ARRAY)):
            bytesString = PSI_NAME_ARRAY[i]
            
            if bytesString == '':
                PSI_POINTERS_ARRAY.append('-1')

            else:
                PSI_POINTERS_ARRAY.append(calcNamePointer(file.tell()))
                
                file.write(bytes.fromhex(bytesString))
        
    #############################################
    # WRITE ENEMY STRINGS & record pointers
    #############################################
        # Skip over the status names... don't want to edit those...
        file.seek(ENEMY_NAME_OFFSET)
        for bytesString in ENEMY_NAME_ARRAY:
            if bytesString == '':
                ENEMY_POINTERS_ARRAY.append('-1')

            else:
                ENEMY_POINTERS_ARRAY.append(calcNamePointer(file.tell()))
                
                file.write(bytes.fromhex(bytesString))
        
    #-------------------------------------------------------------------------------------------
    #############################################
    # WRITE POINTERS OF ITEMS
    #############################################
        for i in range(ITEM_COUNT):
            ptr_bytes = ITEM_POINTERS_ARRAY[i]
            
            if ptr_bytes == '-1':
                continue

            name_writer_offset = ITEM_POS + (8 * i)
            file.seek(name_writer_offset)
            file.write(ptr_bytes)
    #############################################
    # WRITE POINTERS OF TELEPORT / TRAIN NAMES
    #############################################
        for i in range(PLACE_COUNT):
            ptr_bytes = PLACE_POINTERS_ARRAY[i]
            
            if ptr_bytes == '-1':
                continue

            name_writer_offset = TELEPORT_POS + (8 * i)
            file.seek(name_writer_offset)
            file.write(ptr_bytes)

    #############################################
    # WRITE POINTERS OF PSI NAMES
    #############################################
        for i in range(len(PSI_POINTERS_ARRAY)):
            ptr_bytes = PSI_POINTERS_ARRAY[i]
            
            if ptr_bytes == '-1':
                continue

            name_writer_offset = PSI_POS + (8 * i)
            file.seek(name_writer_offset)
            file.write(ptr_bytes)

    #############################################
    # WRITE POINTERS OF ENEMY NAMES
    #############################################
        for i in range(ENEMY_COUNT):
            ptr_bytes = ENEMY_POINTERS_ARRAY[i]
            
            if ptr_bytes == '-1':
                continue

            name_writer_offset = ENEMY_POS + (32 * i) + ENEMY_NAME_PTR_OFFSET
            file.seek(name_writer_offset)
            file.write(ptr_bytes)

    #############################################
        print("Updated all names and pointers of Items, Travel Options, PSI, and Enemies...")


def readHexStrings(starting_offset):
    Output_Array = []

    with open(rom_dir, 'rb') as file:
        file.seek(starting_offset)

        


while(True):
    initialize_thingy_table()
    print('======================================================================')
    print('=========================   TEXT  WRITER   ===========================')
    print('======================================================================')
    print("\n###-----------COMMAND-------------###\n0 - Item Descriptions\n00 - Enemy Descriptions\n1 - All Names\n2 - Hex Translater\n3 - Name Ptr Calc\ne - End Program\n")
    Command = input('Enter a Command: ').lower()

    if Command == 'e':
        break
    elif Command == '0':
        writeDescriptions(item_description_dir, ITEM_DESC_POS)
    elif Command == '00':
        writeDescriptions(enemy_discription_dir, ENEMY_DESC_POS)

    elif Command == '1':
        writeAllNames()
    elif Command == '2':
        # 22 Character limit for battle text
        while(True):
            string = input("\nInput string: ")

            print(translate(string))
        
    elif Command == '3':
        print(calcNamePointer(int(input('\nInput Offset: '), 16)))

    elif Command == '4':
        print( (int.to_bytes(int(input('\nInput Offset: '), 16) - 0x60010, 3, 'little')).hex() )

    elif Command == '5':
        print(calcDescriptionPointer(int(input('\nInput Offset (5): '), 16)))