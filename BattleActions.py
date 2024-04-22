import os
import Utilities as Util

ROOT = os.path.dirname(__file__) + "\\"
### EDITABLES ###
ROM_DIR = ROOT + "Mother Prime.nes"                         # The ROM to read when doing everything

FOLDER_DUMPS = ROOT + "Dumps"
FOLDER_DATA = ROOT + "Data"

DIR_RAW_DUMP = FOLDER_DUMPS + "\\BattleActions Dump.txt"    # Raw Dump in Binary directory
DIR_DUMP = FOLDER_DUMPS + "\\BattleActions.txt"             # Dump in English directory
DIR_COMMON = FOLDER_DUMPS + "\\CommonActions.txt"

DIR_BA_DATA = FOLDER_DATA + "\\BattleActions.txt"           # File to read when Writing to ROM

### CONSTANTS ###
BA_pointers_start = 0x2D80B
BA_pointers_end = 0x2D91C
BA_pointers_len = 0x89 * 2 #BA_pointers_end - BA_pointers_start + 1

BA_data_start = 0x2D91D # Len = 0x112, 0x0 ~ 0x88 actions
BA_targeting_start = 0x2DED7
BA_targeting_len = 0x23
BA_data_end = 0x2deca # idk Bash ptr

BA_extra_data_start = 0x2DFC8 # Extra Space at the end of Targeting
BA_extra_data_end = 0x2E00F
BA_extra_data_len = BA_extra_data_end - BA_extra_data_start + 1

BA_0x88_start = 0x2de6f

### TABLES ###

# Double Hash Table for 1 Hex Commands (like 0X series)
HEX_COMMAND_TABLE = {
    "0" : "END", "2" : "readPSI", "4" : "Effect",
    "9" : "Subroutine", "a" : "Unconditional"
}

HEX_COMMAND_TABLE.update(dict((HEX_COMMAND_TABLE[k], k) for k in HEX_COMMAND_TABLE))

# Double Hash Table for 1 Byte Commands (1X, 3X, 6X, cX)
BYTE_COMMAND_TABLE = {
    "10" : "Spawn", "11" : "animationRun", "12" : "animationSimple", "13" : "animationLong",
    "14" : "callForHelp", "15" : "sproutSeeds", "16" : "escapeBattle", "17" : "animationFire",
    "18" : "animationFreeze", "19" : "animationThunder", "1a" : "animationBeam", "1b" : "animationCrit",
    "30" : "readItem", "31" : "readConsumable", "32" : "readBreakable", "33" : "readBigBag",
    "50" : "Target Nothing", "51" : "Target Selected", "52" : "Target Enemy Team Leader", "53" : "Target Player Team Leader",
    "54" : "Target Self", "55" : "Target Team Leader", "56" : "Target Next",
    "60" : "setNumBash", "61" : "setNumCrit", "62" : "setNum", "63" : "GiegueSpeech", "64" : "applyResistance",
    "65" : "Check", "66" : "playAttackSound", "67" : "animate", "68" : "displayText", "69" : "playSound",
    "c0" : "scriptBreakable", "c1" : "scriptPSIStone", "c2" : "scriptBigBag"
}
# 67 changed from loadSound to animate

BYTE_COMMAND_TABLE.update(dict((BYTE_COMMAND_TABLE[k], k) for k in BYTE_COMMAND_TABLE))

HEX_HEX_TABLE = {"7" : "jumpIf", "8" : "jumpIfNOT","b" : "repeatTimes"}
HEX_HEX_TABLE.update(dict((HEX_HEX_TABLE[k], k) for k in HEX_HEX_TABLE))

# Takes 1 Byte of Argument
USELESS_ARGUMENT_LIST = ["60", "61", "63", "65", "66"]
RAW_ARGUMENT_LIST = ["2", "3", "68", "c"]
POINTER_ARGUMENT_LIST = ["7", "8", "9", "a"]
def hasUselessArg(cmd):
    return bool(USELESS_ARGUMENT_LIST.__contains__(cmd) or USELESS_ARGUMENT_LIST.__contains__(cmd[0]))
def hasRawArg(cmd):
    return bool(RAW_ARGUMENT_LIST.__contains__(cmd) or RAW_ARGUMENT_LIST.__contains__(cmd[0]))

def hasPointerArg(cmd):
    return bool(POINTER_ARGUMENT_LIST.__contains__(cmd) or POINTER_ARGUMENT_LIST.__contains__(cmd[0]))

# complex Arg Tables
TABLE_40 = {
    '00': "Recover HP", '01': "Recover PP", '02': "Raise Speed", '03': "Raise Offense", '04': "Raise Defense", '05': "Max HP",
    '06': "Inflict Damage", '07': "Defense Down PSI", '08': "Lower Fight", '09': "OHKO", '0a': "Cryo Freeze",
    '0b': "Lower Offense", '0c': "Lower Defense", '0d': "Bonus EXP", '0e': "Kill Self", '0f': "Recoil Damage",
    '10': "Edge Closer", '11': "Rage", '12': "Blind", '13': "Poison", '14': "Confuse", '15': "Sleep", '16': 'Para', '17': 'Block',
    '18': 'Guard', '19': 'Shield', '1a': 'Powershield', '1b': 'Bind', '1c': 'Petrify', '1d': 'Asthma', '1e': 'Puzzle',
    '1f':'Heal Poison', '20': 'Heal Sleep', '21': 'Heal Para', '22': 'Heal Asthma', '23': 'Heal Confusion', '24':'Shield Off',
    '25':'Heal Uncon', '26': 'Heal Petrification', '27': 'Magnet', '28': 'Steal Food', '29': 'Sing', '2a': 'Confuse Self'
}

TABLE_64 = { '02':"Light", '04':'Defense Down', '10': 'Electric', '20':'Ice', '40':'Fire'}
TABLE_SOUNDS = { '00':"Nothing", '01':"Attack",'02': "Hit", '03':"Crit", '04':"Thunder",'05':"Fire",'06':"Beam",
                    '07':"Freeze", '08': "Bomb", '09': "Boost", '0a': "Recovery", '0b': "Dodge", '0c':"Dimension Slip",
                    '0d':"Status with Wait", '0e':"Beam2",'0f':"Enemy Attack",'10':"Damage Taken",'11':"Run",
                    '12': "Status",'13': "Miss",'14': "Giegue Attack", '15':"Unconned"}
TABLE_40.update(dict((TABLE_40[k], k) for k in TABLE_40))
TABLE_64.update(dict((TABLE_64[k], k) for k in TABLE_64))
TABLE_SOUNDS.update(dict((TABLE_SOUNDS[k], k) for k in TABLE_SOUNDS))

COMPLEX_ARG_TABLE = {"40": TABLE_40, "64": TABLE_64, "67" : TABLE_SOUNDS, "69" : TABLE_SOUNDS}

def hasComplexArg(cmd):
    return bool(COMPLEX_ARG_TABLE.__contains__(cmd) or COMPLEX_ARG_TABLE.__contains__(cmd[0]))
def getComplexArg(cmd, arg):
    if cmd[0] == "4":
        cmd = "40"
    try:
        return COMPLEX_ARG_TABLE[cmd][arg]
    except Exception:
        return arg
    


# For 7 and 8 Series
TABLE_HEX_ARGS = {"0":"Attacker & Target Alive", "1":"Check Dodge","2":"Check Crit","3":"Check Blind","4":"is in Tank",
                   "5":"has Franklin Badge","6":"Target Alive","7":"Weak to Bug Spray","8":"50% Chance","9":"is Immune Bit",
                   "a":"is Mental Immune Bit", "b":"is Triggered Battle","c":"is Shielded","d":"is Giegue Fight"}
TABLE_HEX_ARGS.update(dict((TABLE_HEX_ARGS[k], k) for k in TABLE_HEX_ARGS))
# c changed from is Player to is Shielded

def getHexArg(cmd):
    if len(cmd) == 2:
        cmd = cmd[1]
    return TABLE_HEX_ARGS[cmd]

POINTER_TABLE = {
    "b79e": "Already Dead Logic",
    "bf9e": "Blind Logic",
    "c49e": "No Effect Logic",
    "ba9e" : "Dodge Logic"
}
POINTER_TABLE.update(dict((POINTER_TABLE[k], k) for k in POINTER_TABLE))

def isStaticPointer(ptr):
    return POINTER_TABLE.__contains__(ptr)

def calcRealLocation(location, distance):
    return Util.calcBattleActionPtr(location + distance)

def isCommand(command):
    if Util.is_hex(command):
        return HEX_COMMAND_TABLE.__contains__(command[0]) or BYTE_COMMAND_TABLE.__contains__(command) or HEX_HEX_TABLE.__contains__(command[0])

    return HEX_COMMAND_TABLE.__contains__(command) or BYTE_COMMAND_TABLE.__contains__(command) or HEX_HEX_TABLE.__contains__(command)

def translateCommand(command):
    if HEX_COMMAND_TABLE.__contains__(command):
        return HEX_COMMAND_TABLE[command]
    if BYTE_COMMAND_TABLE.__contains__(command):
        return BYTE_COMMAND_TABLE[command]
    if HEX_HEX_TABLE.__contains__(command):
        return HEX_HEX_TABLE[command]
    
    if HEX_COMMAND_TABLE.__contains__(command[0]):
        return HEX_COMMAND_TABLE[command[0]] + "0"
    if HEX_HEX_TABLE.__contains__(command[0]):
        return HEX_HEX_TABLE[command[0]] + "0"
    
    return

### Targeting Defines ###
BA_Targeting_0 = "None"         # 00 - No Menu
BA_Targeting_1 = "Ally"         # 01 - Ally Menu
BA_Targeting_2 = "Enemy"        # 10 - Enemy Menu
#BA_Targeting_3 = "Dangerous!"  # 11 - Leads to Bugs
def translateTargeting(t):
    if t == 0:
        return BA_Targeting_0
    elif t == 1:
        return BA_Targeting_1
    elif t == 2:
        return BA_Targeting_2
    
    elif t.strip() == BA_Targeting_0:
        return 0
    elif t.strip() == BA_Targeting_1:
        return 1
    elif t.strip() == BA_Targeting_2:
        return 2
    else:
        return

#----------------------------------------------------------------------------------------------------------------------------------------

def dumpBAsRaw():
    directory = input("Enter wanted ROM File: ")
    if directory.strip() == "":
        directory = ROM_DIR
    with open(DIR_RAW_DUMP, 'w') as file:
        with open(directory, 'rb') as rom:
            rom.seek(BA_pointers_start)
            pointersDump = bytes.hex(rom.read(BA_pointers_len), ",", -2) # splits Pointers by 2 with commas ,
            
            pointersArray = pointersDump.split(',')
            
            # List of Strings (0xHex)
            realLocationsArray = []
            sortedLocationsArray = []
            actionLengthArray = []
            for _, ptr in enumerate(pointersArray):
                realLocationsArray.append(Util.translateBattleActionPtr(ptr)[2:])
                sortedLocationsArray.append(int(Util.translateBattleActionPtr(ptr), 0))

            # Find Battle Action Lengths
            sortedLocationsArray.sort()
            for _, location in enumerate(realLocationsArray):
                integer_location = int(location, 16)

                if sortedLocationsArray.count(integer_location) == 1:
                    idx = sortedLocationsArray.index(integer_location)

                    if idx + 1 < len(sortedLocationsArray):
                        actionLengthArray.append(sortedLocationsArray[idx + 1] - sortedLocationsArray[idx])
                    else:
                        actionLengthArray.append(BA_pointers_end - sortedLocationsArray[idx])

                elif sortedLocationsArray.count(integer_location) > 1:
                    actionLengthArray.append(0)
                    
                else:
                    print("error")
                    quit()

            dumpOutput = ""
            for i, location in enumerate(realLocationsArray):
                rom.seek(int(location, 16))

                dumpOutput += Util.battleActionString(hex(i)) + ", "  + str(pointersArray[i]) + ", " + location + "; "

                for _ in range(actionLengthArray[i]):          
                    dumpOutput += bytes.hex(rom.read(1)) + " "

                dumpOutput += "\n"

            file.write(dumpOutput)

# A more refined version of Dump Battle Actions that writes the data in readable text instead of raw Hex
def dumpBAs():
    directory = input("Enter wanted ROM File: ")
    if directory.strip() == "":
        directory = ROM_DIR
    with open(DIR_DUMP, 'w') as file:
        with open(directory, 'rb') as rom:
            # Read BA Targeting
            rom.seek(BA_targeting_start)
            TargetingArray = []

            for _ in range(BA_targeting_len):
                byte = bin(int.from_bytes(rom.read(1), "big"))[2:].zfill(8)

                TargetingArray.append(int(byte[0:2], 2))
                TargetingArray.append(int(byte[2:4], 2))
                TargetingArray.append(int(byte[4:6], 2))
                TargetingArray.append(int(byte[6:8], 2))

            # Read BA Pointers
            rom.seek(BA_pointers_start)
            pointersDump = bytes.hex(rom.read(BA_pointers_len), ",", -2) # splits Pointers by 2 with commas ,
            
            pointersArray = pointersDump.split(',')
            
            # List of Strings (0xHex)
            realLocationsArray = []
            sortedLocationsArray = []
            actionLengthArray = []
            for _, ptr in enumerate(pointersArray):
                realLocationsArray.append(Util.translateBattleActionPtr(ptr)[2:])
                sortedLocationsArray.append(int(Util.translateBattleActionPtr(ptr), 0))

            # Find Battle Action Lengths
            sortedLocationsArray.sort()
            for _, location in enumerate(realLocationsArray):
                integer_location = int(location, 16)

                if sortedLocationsArray.count(integer_location) == 1:
                    idx = sortedLocationsArray.index(integer_location)

                    if idx + 1 < len(sortedLocationsArray):
                        actionLengthArray.append(sortedLocationsArray[idx + 1] - sortedLocationsArray[idx])
                    else:
                        actionLengthArray.append(BA_pointers_end - sortedLocationsArray[idx])

                elif sortedLocationsArray.count(integer_location) > 1:
                    actionLengthArray.append(0)
                    
                else:
                    print("error line 226")
                    quit()

            out = ""
            LIST_line_locations = []
            for i, location in enumerate(realLocationsArray):
                rom.seek(int(location, 16))
                name = Util.battleActionString(hex(i))
                if name.strip() == "":
                    name = "Action " + hex(i)

                out += name.ljust(30) + " | ID: " + hex(i) + " | Target Menu: " + str(translateTargeting(TargetingArray[i])) + " | " + (location) + "\n"
                LIST_line_locations.append(0)

                # THE DIFFERENCE... READ THE BYTE AND PROCESS THE INFO
                idx = 0
                while idx < (actionLengthArray[i]):
                    out += "\t" #hex(rom.tell()) + " |    "
                    LIST_line_locations.append(rom.tell())

                    b = bytes.hex(rom.read(1))
                    idx += 1

                    if HEX_COMMAND_TABLE.__contains__(b[0]):
                        out += HEX_COMMAND_TABLE[b[0]]

                    elif BYTE_COMMAND_TABLE.__contains__(b):
                        out += BYTE_COMMAND_TABLE[b]

                    elif HEX_HEX_TABLE.__contains__(b[0]):
                        out += HEX_HEX_TABLE[b[0]]

                        if b[0] == "b":
                            out += "; " + b[1]
                        else:
                            out += "; " + getHexArg(b)

                    if hasUselessArg(b):
                        bytes.hex(rom.read(1))
                        idx += 1

                    elif hasRawArg(b):
                        idx += 1
                        out += ": " + bytes.hex(rom.read(1))
                    
                    elif hasComplexArg(b):
                        arg = bytes.hex(rom.read(1))
                        idx += 1
                        out += ": " + getComplexArg(b, arg)
                        

                    elif hasPointerArg(b):
                        ptr = bytes.hex(rom.read(2))
                        idx += 2

                        if isStaticPointer(ptr):
                            ptr = POINTER_TABLE[ptr]
                        else:
                            ptr = Util.translateBattleActionPtr(ptr)
                        
                        out += " -> " + ptr

                    elif b == "62":
                        arg = bytes.hex(rom.read(1))
                        out += ": " + str(int(arg, 16))
                        idx += 1

                    out += "\n" #\t

                out += "\n"
                LIST_line_locations.append(0)
            
            out_2 = []
            for line in out.splitlines(keepends=True):
                if "-> 0x" in line:
                    pointer_hex = line.split("->")[1]
                    pointer_int = int(pointer_hex, 0)
                    
                    # Get the Pointer Line Number
                    if LIST_line_locations.count(pointer_int) > 0:
                        index = LIST_line_locations.index(pointer_int)
                        
                        line = line.split("0x")[0] + "Line " + str(index + 1) + "\n"

                out_2.append(line)
            
            file.writelines(out_2)

            # Write Common Actions
            CA_start = input("Input Common Location Start as Hex: ")
            if CA_start == "":
                quit()
            elif CA_start == "default":
                CA_start = 0x2DEF9
            else:
                CA_start = int(CA_start, 16)
            
            rom.seek(CA_start)
            CA_end = 0x2E00F
            bytestr = "Common Actions\n\t"
            for _ in range(CA_end - CA_start):
                bytestr += bytes.hex(rom.read(1)) + "\n\t"

            file.write(bytestr)


def translateBattleAction(fi):
    with open(fi) as file:
        currBinStr = ""
        for line in file.readlines():
            if line.strip() == "":
                continue

            else:
                # Argument Type
                if line.count(":"):
                    line = line.split(":")
                    
                    cmd = line[0].strip()
                    
                    if HEX_COMMAND_TABLE.__contains__(cmd):
                        cmd = HEX_COMMAND_TABLE[cmd] + "0"
                    elif BYTE_COMMAND_TABLE.__contains__(cmd):
                        cmd = BYTE_COMMAND_TABLE[cmd]
                    
                    arg = line[1].strip()

                    if hasUselessArg(cmd):
                        arg = "00"
                    elif hasComplexArg(cmd):
                        arg = COMPLEX_ARG_TABLE[cmd][arg]
                    elif cmd == "62":
                        arg = hex(int(arg))[2:].zfill(2)


                    currBinStr += cmd + arg
                
                # Hex Hex Type
                elif line.count(";"):
                    if line.__contains__("->"):
                        line = line.split(";")
                        
                        cmd = HEX_HEX_TABLE[line[0].strip()]
                        
                        line = line[1].split("->")
                        arg = TABLE_HEX_ARGS[line[0].strip()]
                        ptr = line[1].strip()

                        if isStaticPointer(ptr):
                            ptr = POINTER_TABLE[ptr]
                        else:
                            ptr = "xxxx"
                        
                        currBinStr += cmd + arg + ptr
                    else:
                        line = line.split(";")

                        currBinStr += HEX_HEX_TABLE[line[0].strip()] + line[1].strip()
                elif line.__contains__("->"):
                    line = line.split("->")
                    cmd = line[0].strip()
                    
                    if HEX_COMMAND_TABLE.__contains__(cmd):
                        cmd = HEX_COMMAND_TABLE[cmd] + "0"
                    
                    ptr = line[1].strip()

                    if isStaticPointer(ptr):
                        ptr = POINTER_TABLE[ptr]
                    else:
                        ptr = "xxxx"
                    
                    currBinStr += cmd + ptr
                else:
                    cmd = line.strip()
                    if HEX_COMMAND_TABLE.__contains__(cmd):
                        cmd = HEX_COMMAND_TABLE[cmd] + "0"
                    elif BYTE_COMMAND_TABLE.__contains__(cmd):
                        cmd = BYTE_COMMAND_TABLE[cmd]

                    currBinStr += cmd

                    if hasUselessArg(cmd):
                        currBinStr += "00"
                
        print(currBinStr)

def readCommonActions(loc):
    with open(DIR_COMMON, 'w') as file:
        with open(ROM_DIR, 'rb') as rom:
            rom.seek(int(loc,16))

            # Print Outs
            line = 1
            out = "CommonAction\t"
            LIST_line_locations = [0]
            idx = 0
            while idx < (0x2e00f - int(loc,16)):
                out += "\t"
                LIST_line_locations.append(rom.tell())

                b = bytes.hex(rom.read(1))
                idx += 1

                if HEX_COMMAND_TABLE.__contains__(b[0]):
                    out += HEX_COMMAND_TABLE[b[0]]

                elif BYTE_COMMAND_TABLE.__contains__(b):
                    out += BYTE_COMMAND_TABLE[b]

                elif HEX_HEX_TABLE.__contains__(b[0]):
                    out += HEX_HEX_TABLE[b[0]]

                    if b[0] == "b":
                        out += "; " + b[1]
                    else:
                        out += "; " + getHexArg(b)

                if hasUselessArg(b):
                    bytes.hex(rom.read(1))
                    idx += 1

                elif hasRawArg(b):
                    idx += 1
                    out += ": " + bytes.hex(rom.read(1))
                
                elif hasComplexArg(b):
                    arg = bytes.hex(rom.read(1))
                    idx += 1
                    out += ": " + getComplexArg(b, arg)
                    

                elif hasPointerArg(b):
                    ptr = bytes.hex(rom.read(2))
                    idx += 2

                    if isStaticPointer(ptr):
                        ptr = POINTER_TABLE[ptr]
                    else:
                        ptr = Util.translateBattleActionPtr(ptr)
                    
                    out += " -> " + ptr

                elif b == "62":
                    arg = bytes.hex(rom.read(1))
                    out += ": " + str(int(arg, 16))
                    idx += 1

                out += "\n" #\t

            out += "\n"
            LIST_line_locations.append(0)
        
        out_2 = []
        for line in out.splitlines(keepends=True):
            if "-> 0x" in line:
                pointer_hex = line.split("->")[1]
                pointer_int = int(pointer_hex, 0)
                
                # Get the Pointer Line Number
                if LIST_line_locations.count(pointer_int) > 0:
                    index = LIST_line_locations.index(pointer_int)
                    
                    line = line.split("0x")[0] + "Line " + str(index + 1) + "\n"

            out_2.append(line)
        
        file.writelines(out_2)

# Writes Battle actions file to ROM
def writeBAs():
    BA_File = open(DIR_BA_DATA, "r") #DATA_DIR

    # Stores Ptr to each line in file
    LinePointersArray = []
    # Stores Names of Each Line
    LineNameTable = {}

    # Stores Data to write to ROM (each line in bytes)
    LineCodeArray = []
    BA_0x88_end = -1

    # Stores BA Data
    BA_PointersArray = []
    BA_TargetMenuArray = []

    # Stores what Lines to Jump at and What Location to
    BA_JumpsArray = {}

    # 0x88's Data
    BA_0x88_targetmenu = -1     # 0x88's TargetMenu
    BA_0x88_end = -1            # 0x88's End (Used to Check its No Zone)
    BA_0x88_ptr = Util.calcBattleActionPtr(BA_0x88_start)

    ###------------------------------------------------ Start Process ------------------------------------------------###
    Location = BA_0x88_start
    currLen = 0
    currLenArray = []
    for i, line in enumerate(BA_File.readlines()):
        currLenArray.append(currLen)
        # Dodge if Line is Empty
        if line.strip() == "":
            LineCodeArray.append("")
            continue

        ### PROCESS BATTLE ACTION ### FOUND HEADER
        if line[0] != "\t" and line.count("|"):
            #id = line.split("ID: ")[1][3:]
            targetMenu = translateTargeting(line.split("Menu: ")[-1])   # "None, Ally, or Enemy -> 0, 1, or 2"

            #-- Special Hard Coded Cases for 0x88, EVE Explosion --#
            # 1st BA Header, 0x88 (hard coded)
            if BA_0x88_targetmenu == -1:
                # Record targetMenu
                BA_0x88_targetmenu = targetMenu
            # 2nd BA Header, probably 0x0 (Process 0x88, Start on Real BAs)
            elif BA_0x88_end == -1:
                # Record 0x88's Line Pointers
                for l in currLenArray:
                    LinePointersArray.append(Util.calcBattleActionPtr(Location + l))
                # Record 0x88's End
                BA_0x88_end = Location + currLen # Location + Len of 0x88
                currLen = 0
                currLenArray.clear()
                # Record Jump & Start on Real BAs
                Location = BA_data_start
                BA_JumpsArray[i] = Location
                # Record 0x0's Start Pointer and Target Menu (Data)
                BA_PointersArray.append(Util.calcBattleActionPtr(Location))
                BA_TargetMenuArray.append(targetMenu)
            
            #-- Process Real BAs beyond 0x0 --#
            else:
                #-- Check for No No Zones & Jump Location --#
                # Data Location 1 <-> 0x88 No Zone
                if Location < BA_0x88_start and Location + currLen > BA_0x88_start:
                    print("Wasted Space in pre-0x88 Area: " + str(BA_0x88_start - Location) + " Bytes At Line: " + str(i) + "\n")
                    Location = BA_0x88_end
                    BA_JumpsArray[i - len(currLenArray)] = Location
                    # Update the BA's Pointer from OOB to new Location
                    BA_PointersArray.pop()
                    BA_PointersArray.append(Util.calcBattleActionPtr(Location))
                # 0x88 <-> Data Location 2 No Zone
                elif Location < BA_data_end - 1 and Location + currLen > BA_data_end - 1:
                    print("Wasted Space in 1st BA Data: " + str(BA_data_end - Location + 1) + " Bytes At Line: " + str(i) + "\n")
                    Location = BA_extra_data_start
                    BA_JumpsArray[i - len(currLenArray)] = Location
                    # Update the BA's Pointer from OOB to new Location
                    BA_PointersArray.pop()
                    BA_PointersArray.append(Util.calcBattleActionPtr(Location))
                # Data Location 2 <-> End of Space... Fail
                elif Location + 1 + currLen > BA_extra_data_end:
                    print("Ran out of space for BA Data.\nExiting...")
                    quit()
                
                #-- Append Previous BA's LinePtrs --#
                for l in currLenArray:
                    LinePointersArray.append(Util.calcBattleActionPtr(Location + l))
                Location += currLen
                currLen = 0
                currLenArray.clear()

                #-- Record BA's Start Pointer and Target Menu --#
                BA_PointersArray.append(Util.calcBattleActionPtr(Location)) # Safe Location not in a No Zone
                BA_TargetMenuArray.append(targetMenu)

            LineCodeArray.append("BA_Header" + line)
            continue
        
        # If Line with a Label
        if line.count("Label ="):
            line, LineName = line.split("Label =")
            LineNameTable[LineName.strip()] = i

        # Dodge if Labeled Line is Empty
        if not (line != "" and line[0] == "\t"):
            LineCodeArray.append("")
            continue

        Command = ""
        Arg = ""
        ByteArg = ""
        Ptr = ""
        # Raw Argument
        if line.strip().startswith("$"):
            currLen += 2
            LineCodeArray.append(line.strip().replace("$", ""))
            continue

        # : # 1 Byte Arg, Len 2
        if line.count(":"):
            currLen += 2
            Command, Arg = line.split(":")
            Command = Command.strip()
            Arg = Arg.strip()

        elif line.count(";"):
            currLen += 1
            
            Command, split_1 = line.split(";")
            Command = Command.strip()

            if split_1.count("->"):
                currLen += 2
                ByteArg, Ptr = split_1.split("->")
                ByteArg = ByteArg.strip()
                Ptr = Ptr.strip()
            else:
                ByteArg = split_1.strip()
        
        elif line.count("->"):
            currLen += 3
            Command, Ptr = line.split("->")
            Command = Command.strip()
            Ptr = Ptr.strip()
        
        else:
            currLen += 1
            Command = line.strip() 

        # Change Command from String to Byte
        if HEX_COMMAND_TABLE.__contains__(Command):
            Command = HEX_COMMAND_TABLE[Command] + "0"
        
        elif BYTE_COMMAND_TABLE.__contains__(Command):
            Command = BYTE_COMMAND_TABLE[Command]

        elif HEX_HEX_TABLE.__contains__(Command):
            Command = HEX_HEX_TABLE[Command]

            # repeatTimes ; X
            if Command == "b":
                Command += ByteArg
            
            # jumpIf, jumpIfNOT 7, 8
            else:
                Command += getHexArg(ByteArg)

        else:
            print("What the Fuck. Something went horribly wrong.\n" +
                  "Error: Unknown command: " + Command)
            exit()

        # Translate Arguments to Byte
        if Command == "62":
            Arg = hex(int(Arg))[2:].zfill(2)
        elif hasUselessArg(Command):
            currLen += 1
            Arg = "00"
        elif hasComplexArg(Command):
            Arg = getComplexArg(Command, Arg)
        #elif hasRawArg(Command):
        #    Arg already obtained
        
        # Translate Pointer to Bytes
        if hasPointerArg(Command):
            if isStaticPointer(Ptr):
                Ptr = POINTER_TABLE[Ptr]
            elif Ptr.count("0x"):
                Ptr = Util.calcBattleActionPtr(Ptr[2:])
            elif isCommand(Ptr):
                Ptr = "Command" + Ptr
            elif Ptr.count("-") and isCommand(Ptr[1:]):
                Ptr = "Command" + Ptr
            elif Ptr.count("Line"): #else Ptr is "Line X"
                pass
            else: #else Ptr is "Custom String"
                Ptr = "Label" + Ptr

        LineCodeArray.append(Command + Arg + Ptr)
    BA_File.close()
    print("Extra Space in 2nd BA Data: " + str(BA_extra_data_end - Location + 1) + " Bytes\n")
    BA_PointersArray.append(BA_0x88_ptr)
    BA_TargetMenuArray.append(BA_0x88_targetmenu)
    ###-------------------- Write the Battle Actions --------------------###
    with open(ROM_DIR, "r+b") as rom:
        rom.seek(BA_0x88_start)
        for i, line in enumerate(LineCodeArray):
            if line == "":
                continue
            
            ### Header ###
            if line.count("BA_Header"):
                # See if the Header is a Jumper
                if BA_JumpsArray.__contains__(i):
                    jumpto = BA_JumpsArray[i]
                    rom.seek(jumpto)
                
                # else ignore, it has no BA commands to write to ROM

            # Process Ptr jumping to "Command"
            elif line.count("Command"):
                line, command = line.split("Command")
                command = command.strip()
                # Negative : Go Backwards to find nearest Command
                if command[0] == "-":
                    command = translateCommand(command[1:])
                    for j in range(i, -1, -1):
                        if LineCodeArray[j].startswith(command):
                            command = LinePointersArray[j]
                            break
                # Positive : Go Forwads to find nearest Command
                else:
                    command = translateCommand(command)
                    for j in range(i, len(LinePointersArray)):
                        if LineCodeArray[j].startswith(command):
                            command = LinePointersArray[j]
                            break

                rom.write(bytes.fromhex(line + command))
            # Process Ptr jumping to "Line X"
            elif line.count("Line"):
                line, lineNum = line.split("Line")
                rom.write(bytes.fromhex(line + LinePointersArray[int(lineNum) - 1]))
            # Write Already Fully Processed Line
            elif Util.is_hex(line):
                rom.write(bytes.fromhex(line))
            # Process Ptr jumping to a Labeled Line
            else:
                line, lineName = line.split("Label")
                line = line.strip()
                lineName = lineName.strip()
                rom.write(bytes.fromhex(line + LinePointersArray[LineNameTable[lineName]]))

            if i > 8 and (rom.tell() < BA_0x88_end and rom.tell() > BA_0x88_start):
                print("Thats illegal!")
                quit()
        ###-------------------- Write Pointers --------------------------- ###
        rom.seek(BA_pointers_start)
        for ptr in BA_PointersArray:
            if len(ptr) != 4:
                print("wtf, Pointers failed: " + ptr)
                exit()
            rom.write(bytes.fromhex(ptr))

        ###-------------------- Write Targeting Menus -------------------- ###
        rom.seek(BA_targeting_start)
        while len(BA_TargetMenuArray) % 4 != 0:
            BA_TargetMenuArray.append(0)
        for i in range(0, len(BA_TargetMenuArray), 4):
            t1, t2, t3, t4 = BA_TargetMenuArray[i:i+4]
            binstr = bin(t1)[2:].zfill(2) + bin(t2)[2:].zfill(2) + bin(t3)[2:].zfill(2) + bin(t4)[2:].zfill(2)
            rom.write(bytes.fromhex( hex(int(binstr, 2))[2:].zfill(2) ))

    print("Wrote all Battle Actions to ROM\n" + ROM_DIR)

# MAIN

command = input("0 - Dump Actions (Raw Bytes)\n1 - Dump Actions (in English)\n2 - Write Actions to ROM\n4 - Read Common Actions\n"
                + "5 - Translate BA from File (gib DIR)\nEnter Command: ")

if command == "0":
    dumpBAsRaw()
elif command == "1":
    dumpBAs()
elif command == '2':
    writeBAs()

elif command == "4":
    readCommonActions(input(" > "))

elif command == '5':
    fi = input("Type File name: ")
    translateBattleAction(fi)