import pprint
import sys

TYPE_COUNT = 46

BASE_ADDRESS = 0x8000

def read_rom(rom, length):
    b = rom.read(length)
    return int.from_bytes(b, byteorder='little')

INSTRUCTIONS = {
    0x00: ('END', ()),
    0x01: ('GOTO', ('offset',)),
    0x02: ('GOSUB', ('word', 'offset')),
    0x03: ('RETURN', ()),
    0x04: ('WAIT', ('bytedec',)),
    0x05: ('ASSERT_FLAG NOT', ('bytedec',)),
    0x06: ('ASSERT_FLAG', ('bytedec',)),
    0x07: ('ILLEGAL_INSTRUCTION_07', ()),
    0x08: ('TEXT', ('word',)),
    0x09: ('YES_NO_SELECTION', ('offset',)),
    0x0A: ('GOTO_UNLESS_TALKING', ('offset',)),
    0x0B: ('GOTO_UNLESS_CHECKING', ('offset',)),
    0x0C: ('GOTO_UNLESS_USING_PSI', ('byte', 'offset')),
    0x0D: ('GOTO_UNLESS_USING_ITEM', ('byte', 'offset')),
    0x0E: ('ILLEGAL_INSTRUCTION_0E', ()),
    0x0F: ('RESET_GAME', ()),
    0x10: ('SET_FLAG', ('bytedec',)),
    0x11: ('CLEAR_FLAG', ('bytedec',)),
    0x12: ('GOTO_UNLESS_FLAG', ('bytedec', 'offset')),
    0x13: ('DEC_COUNTER', ('bytedec',)),
    0x14: ('INC_COUNTER', ('bytedec',)),
    0x15: ('ZERO_COUNTER', ('bytedec',)),
    0x16: ('GOTO_IF_COUNTER_LESS_THAN', ('bytedec', 'bytedec', 'offset')),
    0x17: ('SET_VARIABLE', ('bytedec', 'bytedec')),
    0x18: ('CHARACTER_SELECTION_MENU', ('offset',)),
    0x19: ('LOAD_CHARACTER', ('bytedec',)),
    0x1A: ('GOTO_UNLESS_CHARACTER_SELECTED', ('bytedec', 'offset')),
    0x1B: ('GOTO_IF_NO_DAD_MONEY', ('offset',)),
    0x1C: ('NUMBER_INPUT', ('offset',)),
    0x1D: ('LOAD_NUMBER', ('worddec',)),
    0x1E: ('GOTO_IF_NUMBER_LESS_THAN', ('worddec', 'offset')),
    0x1F: ('SHOW_WALLET', ()),
    0x20: ('ITEM_SELECTION_MENU', ('offset',)),
    0x21: ('STORAGE_SELECTION_MENU', ('offset',)),
    0x22: ('LIST_SELECTION_MENU', ('byte', 'byte', 'byte', 'byte', 'offset')),
    0x23: ('GOTO_CHARACTER_HAS_ITEM', ('byte', 'offset')),
    0x24: ('GOTO_UNLESS_ITEM_IN_STORAGE', ('byte', 'offset')),
    0x25: ('LOAD_ITEM', ('byte',)),
    0x26: ('GOTO_UNLESS_ITEM_IS', ('byte', 'offset')),
    0x27: ('GOTO_UNLESS_ANYONE_HAS_ITEM', ('byte', 'offset')),
    0x28: ('GIVE_MONEY', ('offset',)),
    0x29: ('TAKE_MONEY', ('offset',)),
    0x2A: ('DEPOSIT_TO_BANK', ('offset',)),
    0x2B: ('WITHDRAW_FROM_BANK', ('offset',)),
    0x2C: ('GOTO_UNLESS_SELLABLE', ('offset',)),
    0x2D: ('GIVE_ITEM', ('offset',)),
    0x2E: ('TAKE_ITEM', ('offset',)),
    0x2F: ('ADD_ITEM_TO_STORAGE', ('offset',)),
    0x30: ('REMOVE_ITEM_FROM_STORAGE', ('offset',)),
    0x31: ('LOAD_ITEM_FROM_INVENTORY', ('bytedec', 'offset')),
    0x32: ('MULTIPLY_BY_NUMBER_OVER_100', ('bytedec')),
    0x33: ('GOTO_IF_CHARACTER_ABSENT', ('bytedec', 'offset')),
    0x34: ('UNKNOWN_34', ()),
    0x35: ('GOTO_UNLESS_TOUCHING', ('offset',)),
    0x36: ('GOTO_UNKNOWN_36', ('offset',)),
    0x37: ('MENU_SELECTION', ('word', 'offset', 'offset')),
    0x38: ('GOTO_IF_INVENTORY_EMPTY', ('offset',)),
    0x39: ('GOTO_IF_STORAGE_EMPTY', ('offset',)),
    0x3A: ('LOAD_CHARACTER_FROM_PARTY', ('bytedec', 'offset')),
    0x3B: ('SET_OBJECT_TYPE', ('bytedec')),
    0x3C: ('UNKNOWN_3C', ()),
    0x3D: ('TELEPORT_PLAYER', ('coordinates',)),
    0x3E: ('MOVE_OBJECT', ('word',)),
    0x3F: ('SIGNAL_OBJECT', ('bytedec',)),
    0x40: ('GOTO_UNLESS_SIGNALED', ('offset',)),
    0x41: ('TELEPORT_TO_SAVE_LOCATION', ()),
    0x42: ('ADD_CHARACTER_TO_PARTY', ('bytedec', 'offset')),
    0x43: ('REMOVE_CHARACTER_FROM_PARTY', ('bytedec', 'offset')),
    0x44: ('START_BATTLE', ('bytedec',)),
    0x45: ('MULTIPLY_BY_AMOUNT_OF_CHARACTERS', ()),
    0x46: ('ROCKET', ('bytedec',)),
    0x47: ('AIRPLANE', ('bytedec',)),
    0x48: ('TANK', ('bytedec',)),
    0x49: ('BOAT', ('bytedec',)),
    0x4A: ('TRAIN', ()),
    0x4B: ('ELEVATOR', ('bytedec',)),
    0x4C: ('NO_VEHICLE', ('bytedec',)),
    0x4D: ('UNKNOWN_4D', ()),
    0x4E: ('UNKNOWN_4E', ()),
    0x4F: ('GOTO_UNKNOWN_4F', ('offset',)),
    0x50: ('GOTO_UNLESS_MAX_HP', ('offset',)),
    0x51: ('HEAL_HP', ('bytedec',)),
    0x52: ('GOTO_IF_CHARACTER_HAS_STATUS', ('byte', 'offset')),
    0x53: ('KEEP_ONLY_STATUSES', ('byte',)),
    0x54: ('GOTO_UNLESS_LEVEL', ('bytedec', 'offset')),
    0x55: ('SPEND_NIGHT', ()),
    0x56: ('SAVE_GAME', ()),
    0x57: ('GET_NEEDED_EXP', ()),
    0x58: ('GET_WALLET_MONEY', ()),
    0x59: ('INFLICT_STATUS', ('byte',)),
    0x5A: ('CHANGE_MUSIC', ('bytedec',)),
    0x5B: ('PLAY_SOUND_1', ('bytedec',)),
    0x5C: ('PLAY_SOUND_2', ('bytedec',)),
    0x5D: ('PLAY_SOUND_3', ('bytedec',)),
    0x5E: ('ILLEGAL_INSTRUCTION_5E', ()),
    0x5F: ('LEARN_TELEPORTATION', ()),
    0x60: ('GOTO_UNLESS_MAX_PP', ('offset',)),
    0x61: ('REPLENISH_PP', ('bytedec',)),
    0x62: ('CONFISCATE_WEAPON', ('offset',)),
    0x63: ('SELECT_CONFISCATED_WEAPON', ('offset',)),
    0x64: ('LIVE_SHOW_SEQUENCE', ()),
    0x65: ('GOTO_UNLESS_LEARNED_ALL_MELODIES', ('offset',)),
    0x66: ('REGISTER_PLAYERS_NAME', ()),
    0x67: ('DARKEN_PALETTE', ()),
    0x68: ('LANDMINE', ()),
    0x69: ('HORIZONTAL_SHAKE', ()),
    0x6A: ('XX_CRYSTAL', ())
}

def dump_script(ptr, objdata, startoffset):
    out = ''
    i = startoffset
    end = len(objdata)
    endptr = ptr + len(objdata)
    has_movement_data = False
    try:
        while i < end:
            out += f'L_{i:02X}: '

            op = objdata[i]
            i += 1

            instruction = INSTRUCTIONS.get(op, (f'BAD_INSTRUCTION_{op:02X}', ()))
            out += instruction[0]

            for argtype in instruction[1]:
                if argtype in ('offset', 'byte', 'bytedec'):
                    arg = objdata[i]
                    i += 1
                else:
                    arg = (objdata[i+1] << 8) | objdata[i+0]
                    i += 2

                out += ' '
                if argtype == 'offset':
                    out += f'L_{arg:02X}'
                elif argtype == 'byte':
                    out += f'0x{arg:02X}'
                elif argtype in ('bytedec', 'worddec'):
                    out += f'{arg}'
                elif argtype == 'word':
                    out += f'0x{arg:04X}'
                elif argtype == 'coordinates':
                    # Hacky lol
                    arg2 = (objdata[i+1] << 8) | objdata[i+0]
                    i += 2

                    xloc = (arg & 0xFFC0) >> 2
                    yloc = ((arg2 & 0xFFC0) - 0x2000) >> 2
                    out += f'{xloc} {yloc} ; 0x{arg:04X} 0x{arg2:04X}'

            if op == 0x3E: # MOVE_OBJECT
                # Hacky shit taking advantage of Python's epic scoping rules
                has_movement_data = True
                arg -= 0x8000
                if endptr > arg:
                    endptr = arg
                    end = arg - ptr

            out += '\n'
            if op in (0x00, 0x03):
                out += '\n'
    except IndexError:
        pass

    if has_movement_data:
        out += f'MOVEMENT DATA: {objdata[end:].hex()}'

    return out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(f'Usage: {sys.argv[0]} ebb_rom')

    types = {i: 0 for i in range(TYPE_COUNT)}

    type_scriptstart = []
    with open(sys.argv[1], 'rb') as rom:
        rom.seek(31*0x2000 + 0x0105 + 3 + 0x10)
        for i in range(TYPE_COUNT):
            type_scriptstart.append(read_rom(rom, 1) & 0x0F)
            read_rom(rom, 3) # Ignored

        for bank in range(3):
            print(f'BANK #{bank+16} START')
            rom.seek(0x20000+(bank * 0x2000)+16)
            data = rom.read(0x2000) # A whole bank
            master_table = []

            i = 0
            ptr = (data[i+1] << 8) | data[i+0]
            while ptr >= 0x8000 and ptr < 0xA000:
                master_table.append(ptr)
                i += 2
                ptr = (data[i+1] << 8) | data[i+0]

            subtables = []
            subaddr = []
            for i, address in enumerate(master_table):
                subaddr.append(address)
                ptrs = []
                j = address - BASE_ADDRESS
                ptr = (data[j+1] << 8) | data[j]
                while ptr >= 0x8000 and ptr < 0xA000:
                    ptrs.append(ptr)
                    j += 2
                    ptr = (data[j+1] << 8) | data[j]

                subtables.append(ptrs)

            for i, subtable in enumerate(subtables):
                print(f'Area #{i:02d} START @ ${subaddr[i]:04X} (file {(bank+16)*0x2000+16+subaddr[i]:05X})')
                for objnum in range(len(subtable)-1):
                    ptr = subtable[objnum] - BASE_ADDRESS
                    ptrnext = subtable[objnum+1] - BASE_ADDRESS
                    objdata = data[ptr:ptrnext]
                    type_ = objdata[0] & 0x3F
                    xloc = ((objdata[1] << 8) | (objdata[0] & 0xC0)) >> 2
                    direction = objdata[2] & 0x3F
                    yloc = (((objdata[3] << 8) | (objdata[2] & 0xC0)) - 0x2000) >> 2

                    types[type_] += 1

                    datstr = f'type={type_}, xloc={xloc}, direction={direction}, yloc={yloc}'
                    print(f'    Object #{objnum:02d} @ ${ptr:04X} (file {(bank+16)*0x2000+16+ptr:05X})')
                    print(f'        {datstr}')

                    scriptstart = type_scriptstart[type_]
                    if type_ in (1, 2, 3, 4): # DOOR
                        music = objdata[4] & 0x3F
                        targetx = ((objdata[5] << 8) | (objdata[4] & 0xC0)) >> 2
                        targetdirection = objdata[6] & 0x3F
                        targety = (((objdata[7] << 8) | (objdata[6] & 0xC0)) - 0x2000) >> 2
                        print(f'        music={music}, targetx={targetx}, targetdirection={targetdirection}, targety={targety}')
                    elif type_ == 32:
                        print(f'        EXTRA HEADER: {objdata[4:8].hex()}')
                    elif type_ != 24:
                        print(f'        EXTRA HEADER: {objdata[4:6].hex()}')
                    if scriptstart > 0 and scriptstart < len(objdata):
                        out = dump_script(ptr, objdata, scriptstart)
                        print(f'SCRIPT:\n{out}\n')
                        #print(f'        SCRIPT: {objdata[scriptstart:].hex()}')

                    print(f'        TOTAL {len(objdata)} BYTES\n\n')
                print(f'Area #{i:02d} END\n')

            #print(', '.join(f'{ptr:04X}' for ptr in master_table))
            #print(subtables)
            print(f'BANK #{bank+16} END\n\n\n')

        #pprint.pprint(types)
