import os
#import Translator.ThingyTableTranslate

### EDITABLES ###
rom_name = "Mother Prime.nes"
strings_folder = 'InternalStrings'
translator_folder = 'Translator'
data_folder = "Data/"
dumps_folder = "Dumps"

item_name_dir = strings_folder + "/ItemNames.txt"
psi_name_dir = strings_folder + "/PSINames.txt"
enemy_name_dir = translator_folder + "/Enemy Names.txt"
battle_name_dir = strings_folder + "/BAStrings.txt"
presents_dir = data_folder + "Presents.txt"

enemy_group_name_dir = strings_folder + "/EnemyGroupStrings.txt"

# Raw Maths

def is_hex(s):
    for chara in s:
        if not " 0123456789abcdef".__contains__(chara.lower()):
            return False
    
    return True
    

def calc3BytePtr(description_offset):
    return int.to_bytes(description_offset - int('60010', 16), 3, 'little')

# Returns a 2 byte Pointer
def calcNamePointer(name_offset):
    return int.to_bytes(name_offset + int('7ff0', 16), 2, 'little')

def calcPointer(off):
    return int.to_bytes(off - 0x60010, 3, 'little')

# Given a real (byteorder big) integer, returns a translated Pointer as int
def calc_intPtr_To_Real(ptr):
    return hex(ptr + 0x60010)

def add_30Myriad(ptr):
    return hex(int(ptr, 16) + 0x30010)

# Battle Action Ptr (size 2, Big order) --> Real Location in ROM
def translateBattleActionPtr(ptr):
    ptr = ptr[2:] + ptr[:2] # Reverse the Order of Bytes
    return hex(int(ptr, 16) + 0x24010) 

# Real Location in ROM --> Battle Action Ptr (size 2)
def calcBattleActionPtr(rom_location):
    if type(rom_location) == int:
        ptr = hex(rom_location - 0x24010)[2:]
    else:
        ptr = hex(int(rom_location, 16) - 0x24010)[2:].zfill(4)
    return ptr[2:] + ptr[:2]


# Strings
BattleActions = []
def battleActionString(hex_id):
    if len(BattleActions) == 0:
        with open(battle_name_dir, 'r') as file:
            for line in file:
                BattleActions.append(line.strip())

    try:
        return BattleActions[int(hex_id, 16)]
    except Exception:
        return "" #Nothing
