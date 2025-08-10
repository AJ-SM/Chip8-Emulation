import numpy as np 
from typing import * # Remove this to specifinces Before Pushing anywhere 

# Some CPU sepcific initial data
max_memo:int = 4
no_regs:int = 16
stackLength:int = 16
no_keys:int = 16

''' Why uint8 ?
    Since our Each Instruction is of 1 byte (8bits) so we need some data type to store 2^8 (256) 
    instruction and uint8 = UnsignedIntegerOf8bits (0~255)- (00~FF) seems to be the great choice  '''

memory = np.array(max_memo*1024).astype(np.uint8)
stack = np.array(stackLength).astype(np.uint8)
hex_keypad = np.array(16)
opcode = 0000

''' since we only need to point form 0 ~ 4095 *(000~FFF) using 16bits is bit waste of memory
    because 12bits which we need not there in nmpy..'''

reg_index= np.uint16(0)
reg_pc= np.uint16(0) 
reg_delayTimer = np.uint16(0)
reg_soundTimer = np.uint16(0) # Won't Be using it probably
reg_stackPointer = np.uint(0) # just indexs of the stack 


'''
        0x000-0x1FF - Chip 8 interpreter (contains font set in emu)
        0x050-0x0A0 - Used for the built in 4x5 pixel font set (0-F)
        0x200-0xFFF - Program ROM and work RAM

'''





# Quick Note : Everything over here is zero Indexed