import os
import Utilities as Util

### PATHS ###
script_dir = os.path.dirname(__file__) + "\\"
DIR_ROM = script_dir + "Mother Prime.nes"
thingy_table_dir = script_dir + "TextTool/ThingyTable.txt"
command_dir = script_dir + "TextTool/Commands.txt"

item_description_dir = script_dir + "TextTool/Strings/ItemDesc.txt"
enemy_discription_dir = script_dir + "TextTool/Strings/EnemyDesc.txt"
item_name_dir = script_dir + "TextTool/Strings/ItemName.txt"
teleport_name_dir = script_dir + "TextTool/Strings/PlaceName.txt"
psi_name_dir = script_dir + "TextTool/Strings/PSIName.txt"
enemy_name_dir = script_dir + "TextTool/Strings/EnemyName.txt"
all_text_dir = script_dir + "TextTool/AllText.txt"

# Text Dumper
DIR_DUMP = script_dir + "Dumps/AllText.txt"
DIR_WRITE = script_dir + "TextTool/AllText.txt"

DEFAULT_STRING = "System Error!!!"
DEFAULT_PTR = 0x0
DEFAULT_LOCATION = DEFAULT_PTR + 0x60010

### CONSTANTS ###
WRITE_START_POS = 0x11
WRITE_AVOID_START = 0x608
WRITE_AVOID_END = 0x641
WRITE_START2_POS =  WRITE_AVOID_END + 1
WRITE_START3_POS = 0xa05

TEXT_OFFSET = 0x60010
TEXT_POINTERS_OFFSET = 0x30010 + 3

text_lines_count = 0x0729

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


ITEM_COUNT = int('7f', 16)
PLACE_COUNT = 40
PSI_COUNT = 63
ENEMY_COUNT = 122

BATTLE_TEXT_OFFSET = 0xb78e01

### GLOBALS ###

# Stores Single-Byte Characters
BYTE_LIST = []

# Stores Multi-Byte Characters
MULTI_TABLE = {}
def potentialMulti(byte):
    for multi in MULTI_TABLE:
        if multi.startswith(byte):
            return True
    
    return False

# Stores Commands
COMMAND_TABLE = {
    "00":"<END>",
    "01":"\n",
    "02":"\\p",
    "03":"\\b",
    "05":"<NOP>",
}

# Stores Commands with Arguments
ARGUMENT_TABLE = {
    "04":"goTo",
    "20":"setPos",
    "21":"printStr",
    "22":"repeat",
    "23":"printNum",
}


LABELED_COMMAND_TABLE = {}

def isCommand(byte: str):
    byte = byte.strip()
    return byte in COMMAND_TABLE or byte in ARGUMENT_TABLE

def getArgSize(command: str):
    if command in COMMAND_TABLE:
        return 0
    if command in {"04","20","21","22",}:
        return 2
    if command in {"23","24"}:
        return 4

# Command, Arg (Bytes) -> (String)
def translateArgs(command: str, arg: str):
    if arg == "":
        return COMMAND_TABLE[command]

    command_str = ARGUMENT_TABLE[command]
    return "[{} -> {}]".format(command_str, arg)


def initialize_thingy_table():
    tableFile = open(thingy_table_dir, "r")
    for line in tableFile:
        hexval, strval = line.split('=', 1)
        hexval = hexval.lower()
        # Read Space (Hardcoded A0)
        if hexval == "a0":
            BYTE_LIST.append((hexval, " "))
        # Normal 1 Byte 1 Char Thingy
        elif len(hexval) == 2:
            BYTE_LIST.append((hexval, strval.strip()))

        else:
            MULTI_TABLE[hexval] = strval.strip()

    tableFile.close()

    commandFile = open(command_dir, "r")
    for line in commandFile:
        hexval, strval = line.split('=', 1)
        hexval = hexval.lower()
        LABELED_COMMAND_TABLE[hexval] = strval.strip()

    commandFile.close()

    # Sort Bytetable by Large Characters first so they get priority when Translating between Byte & String
    BYTE_LIST.sort(key=lambda g: len(g[1]), reverse=True)

    global BYTE_TABLE
    BYTE_TABLE = dict(BYTE_LIST)
    BYTE_TABLE.update(dict((BYTE_TABLE[k], k) for k in BYTE_TABLE))

def is_hex(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def startsWithArgument(String):
    for byte, s in list(ARGUMENT_TABLE.items()):
        if String.startswith("[" + s):
            return byte, s
    return False

def startsWithLabel(String):
    for byte, s in list(LABELED_COMMAND_TABLE.items()):
        if String.startswith(s):
            return byte, s
    return False

def startsWithCommand(String):
    for byte, s in list(COMMAND_TABLE.items()):
        if String.startswith(s):
            return byte, s
    return False

def startsWithMulti(String):
    for byte, s in list(MULTI_TABLE.items()):
        if String.startswith(s):
            return byte, s
    return False

def startsWithByte(String):
    for byte, s in BYTE_LIST:
        if String.startswith(s):
            return byte, s
    return False

# String -> Bytecodes
def stringToBytes(String: str, toggle_quotes: bool = False):
    Bytecode = ""
    
    # Can't use str.replace() because Bytecode and String could (theoretically) have the same values
    while len(String) != 0:
        # At the Start of the remaining (untranslated) String...
        # Unlabeled Commands with Arguments
        if goto := startsWithArgument(String):
            byte, str = goto
            index = String.find("[" + str + " ->")
            end = String.find("]", index)
            arg = String[end-5:end]

            String = String[end+1:]
            Bytecode += byte + arg
        
        elif goto := startsWithLabel(String):
            byte, str = goto
            String = String[len(str):]
            Bytecode += byte

        elif goto := startsWithCommand(String):
            byte, str = goto
            String = String[len(str):]
            Bytecode += byte

        elif goto := startsWithMulti(String):
            byte, str = goto
            String = String[len(str):]
            Bytecode += byte
        
        # Special Case for Quotations "
        elif String[0] == '"':
            String = String[1:]
            if toggle_quotes:
                Bytecode += BYTE_TABLE['"2']
            else:
                Bytecode += BYTE_TABLE['"1']
            toggle_quotes = not toggle_quotes
        # Normal 1 Byte 1 Char Thingys
        elif goto := startsWithByte(String):
            byte, str = goto
            Bytecode += byte
            String = String[len(str):]

    return Bytecode, toggle_quotes

# Bytecode -> String
def bytesToString(bytecode):
    pass

# Dumps all Text to Dump Location
def dumpText():
    rom = open(DIR_ROM, 'rb')
    rom_pointers = open(DIR_ROM, 'rb')
    rom.seek(TEXT_OFFSET)
    rom_pointers.seek(TEXT_POINTERS_OFFSET)

    with open(DIR_DUMP, 'w') as file:
        print("Started working on reading the text...\n")
        
        for i in range(1, text_lines_count):
            ptr = int.from_bytes(rom_pointers.read(3), byteorder="little")

            # Translate: Pointer (int) -> Real Location in ROM (hex)
            location = Util.calc_intPtr_To_Real(ptr)
            
            if location == 0:
                continue
            
            rom.seek(ptr + 0x60010)

            # Write a Header
            file.write("# " + hex(i)[2:].zfill(4) + " #\n")

            # Parse the Bytecode & Write to File
            while(True):
                Byte = bytes.hex(rom.read(1)).zfill(2)
                
                # if Command
                if isCommand(Byte):
                    # if the Command is <END>
                    if Byte == "00":
                        file.write("\n")
                        break
                    
                    Arg = ""
                    for _ in range(getArgSize(Byte)):
                        Arg += bytes.hex(rom.read(1)).zfill(2)

                    # if the Command + Arg is Labeled
                    if Byte + Arg in LABELED_COMMAND_TABLE:
                        file.write(LABELED_COMMAND_TABLE[Byte + Arg])
                    
                    else:
                        file.write(translateArgs(Byte, Arg))
                
                # Byte is a potential Multi-Byte
                elif potentialMulti(Byte):
                    while(True):
                        Byte += bytes.hex(rom.read(1)).zfill(2)
                        if Byte in MULTI_TABLE:
                            file.write(MULTI_TABLE[Byte])
                            break
                # Byte is a normal 1 Byte
                else:
                    if Byte in BYTE_TABLE:
                        if BYTE_TABLE[Byte] in {'"1', '"2'}:
                            file.write('"')
                        else:
                            file.write(BYTE_TABLE[Byte])
                    
                    else:
                        file.write("(" + Byte + ")")
        
        print(" >>> Finished dumping all of the text!")
    rom.close()
    rom_pointers.close()

# Writes all Text
def writeText():
    file = open(DIR_WRITE, 'r')
    pointerArray = []
    with open(DIR_ROM, 'r+b') as rom:
        print("Started writing...\n")
        rom.seek(TEXT_OFFSET)
        
        currentBytestr = ""
        toggle_quotes = False
        for line in file:
            # if Line is Header
            if line.strip().startswith("#") and line.strip().endswith("#"):
                if len(currentBytestr.strip()) != 0:
                    currentBytestr = currentBytestr[:-2]
                    currentBytestr += "00" # Add END to end of String
                    rom.write(bytes.fromhex(currentBytestr))
                    currentBytestr = ""
                #ID = line.strip("#").strip() - unused
                pointerArray.append(Util.calc3BytePtr(rom.tell()))
                continue

            elif line.strip() == DEFAULT_STRING:
                continue

            # Translate String
            resultStr, toggle_quotes = stringToBytes(line, toggle_quotes)
            currentBytestr += resultStr
        
        rom.seek(TEXT_POINTERS_OFFSET)
        for ptr in pointerArray:
            rom.write(ptr)
        
        print(" >>> Finished writing all of the text!")
    file.close()


# Returns a 3 byte Pointer
def calcDescriptionPointer(description_offset):
    return int.to_bytes(description_offset - int('60010', 16), DESC_PTR_LENGTH, 'little')

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
            ITEM_NAME_ARRAY.append(stringToBytes(line.strip())[0] + '00')
    with open(teleport_name_dir, 'r') as file:
        for line in file:
            PLACE_NAME_ARRAY.append(stringToBytes(line.strip())[0] + '00')
    with open(psi_name_dir, 'r') as file:
        for line in file:
            PSI_NAME_ARRAY.append(stringToBytes(line.strip())[0] + '00')
    with open(enemy_name_dir, 'r') as file:
        for line in file:
            ENEMY_NAME_ARRAY.append(stringToBytes(line.strip())[0] + '00')

def writeItemNames():
    ITEM_POINTERS_ARRAY = []
    with open(DIR_ROM, 'r+b') as file:
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

    with open(DIR_ROM, 'r+b') as file:
    #############################################
    ### WRITE ITEM STRINGS & record pointers
    #############################################
        file.seek(WRITE_START_POS)
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
        for i in range(len(PSI_NAME_ARRAY)):
            bytesString = PSI_NAME_ARRAY[i]
            
            if bytesString == '':
                PSI_POINTERS_ARRAY.append('-1')

            else:
                if file.tell() < WRITE_AVOID_START and len(bytesString) > WRITE_AVOID_START - file.tell():
                    file.seek(WRITE_START3_POS)
                
                PSI_POINTERS_ARRAY.append(calcNamePointer(file.tell()))
                file.write(bytes.fromhex(bytesString))
        
    #############################################
    # WRITE ENEMY STRINGS & record pointers
    #############################################
        # Skip over the status names... don't want to edit those...
        file.seek(WRITE_START2_POS)
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

    with open(DIR_ROM, 'rb') as file:
        file.seek(starting_offset)

def replaceText():
    old = input("Enter String to replace: ")
    new = input("Enter String to replace with: ")

    with open(all_text_dir, "r+") as file:
        allText = file.read().replace(old, new)

        file.write(allText)


while(True):
    initialize_thingy_table()
    print('======================================================================')
    print('=========================   TEXT  WRITER   ===========================')
    print('======================================================================')
    print("\n###-----------COMMAND-------------###\n1 - Write All Names"
        + "\n2 - Hex Translater\n3 - Name Ptr Calc\n6 - Replace Characters\n8 - Dump All Text\n9 - Write all Text"
        + "\ne - End Program\n")
    Command = input('Enter a Command: ').lower()

    if Command == 'e':
        break
    elif Command == '1':
        writeAllNames()
    elif Command == '2':
        # 22 Character limit for battle text
        while(True):
            string = input("\nInput string: ")

            print(stringToBytes(string))
        
    elif Command == '3':
        print(calcNamePointer(int(input('\nInput Offset: '), 16)))

    elif Command == '4':
        print( (int.to_bytes(int(input('\nInput Offset: '), 16) - 0x60010, 3, 'little')).hex() )

    elif Command == '5':
        print(calcDescriptionPointer(int(input('\nInput Offset (5): '), 16)))

    elif Command == '6':
        replaceText()

    elif Command == "8":
        dumpText()
    elif Command == '9':
        writeText()