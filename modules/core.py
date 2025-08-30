import random
import numpy as np
import time
import sys

# Some CPU sepcific initial data
max_memo:int = 4096 # Corrected from 4 to 4096
no_regs:int = 16
stackLength:int = 16
no_keys:int = 16

# NOTE: The global variables below were moved into the Chip8 class `__init__` method
# for better organization and to avoid global state issues. Your comments are preserved here.

''' Why uint8 ?
    Since our Each Instruction is of 1 byte (8bits) so we need some data type to store 2^8 (256) 
    instruction and uint8 = UnsignedIntegerOf8bits (0~255)- (00~FF) seems to be the great choice  '''

# memory = [0] * 4096
# stack = np.array(stackLength).astype(np.uint8) # Corrected initialization inside the class
# hex_keypad = np.array(16)
# opcode = 0000

''' since we only need to point form 0 ~ 4095 *(000~FFF) using 16bits is bit waste of memory
    because 12bits which we need not there in nmpy..'''

# reg_index= np.uint16(0)
# reg_pc= np.uint16(0) 
# reg_delayTimer = np.uint16(0)
# reg_soundTimer = np.uint16(0) # Won't Be using it probably
# reg_stackPointer = np.uint(0) # just indexs of the stack

'''
        0x000-0x1FF - Chip 8 interpreter (contains font set in emu)
        0x050-0x0A0 - Used for the built in 4x5 pixel font set (0-F)
        0x200-0xFFF - Program ROM and work RAM

'''

# Quick Note : Everything over here is zero Indexed
class Chip8():
    def __init__(self):
        self.pc = 0x200 # Set initial PC to 0x200
        self.opcode = 0
        self.I = 0 # Renamed from reg_index
        self.sp = 0 # Renamed from reg_stackPointer
        self.memory = bytearray(max_memo)

        # FIX: Correctly initializing the stack as an array of 16 zeros
        self.stack = np.zeros(stackLength, dtype=np.uint16)

        self.v = bytearray(no_regs) # TODO Do type checking before uploading
        # self.chipfontset = [1,12] # This line was commented out as it's part of loadfontset now
        
        # also including timers
        self.sound_timer = 0 # Renamed from reg_soundTimer
        self.delay_timer = 0 # Renamed from reg_delayTimer
        
        # Dont Want to poplulate these all over the palce
        # FIX: Renamed `screen` to `gfx` for clarity, as it's the graphics buffer
        self.gfx = [0] * (64*32)
        self.draw_flag = False
        self.key = [0] * no_keys
        
        # Load the fontset into memory on creation
        self.loadfontset()

    def reset(self):
        self.pc = 0x200 # Corrected from hex(0x200) to an integer
        self.opcode = 0
        self.I=0
        self.sp=0
        # todos :  Clear display
        self.gfx = [0] * (64*32)
        # todos :  Clear stack
        self.stack = np.zeros(stackLength, dtype=np.uint16)
        #  todos : Clear registers V0-VF
        self.v = bytearray(no_regs)
        # todos :  Clear memory - Note: In a real reset, memory isn't fully cleared, only program area.
        # todos : loading fontset
        # This loop was in the original code, but `self.chipfontset` is not defined.
        # The font set is now loaded correctly via loadfontset().
        # for i in range(80):
        #     self.memory[i]=self.chipfontset[i]
        self.loadfontset() # Correct way to load the fontset
        # todos :  reset timers
        self.delay_timer = 0
        self.sound_timer = 0

    def loadfontset(self):
        ''' Have to load the font-set into memory so that we can read the font and render it..'''
        self.fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]
        
        # loading the font into memory for location 0x000 (Note: typically starts at 0x50)
        for i in range(len(self.fontset)):
            self.memory[i + 0x50] = self.fontset[i] # FIX: fontset loaded at 0x50

    def loadRom(self,path):
        ''' Load the file for the given path or file name then store the program form 
            memory address 0x200 (512) onward just iterating on the file and storing 
            the data in memory '''
        
        with open(path,"rb") as f:
            rom_data = f.read()
            for i, byte in enumerate(rom_data):
                self.memory[0x200 + i] = byte

    def emulateCycle(self):
        ''' This Function will trigger the Fetch, Decode and Execute operation of 
            one opcode which is specified by the address form the PC, since the Chip8
            has the opcode of 2 bytes so we will run it FDE cycle twiced '''
        
        # Feteching the opcode and create 16 bit form  2 * 8 bit..
        self.opcode = self.memory[self.pc] << 8 | self.memory[self.pc+1]
        self.Decode_Execute(self.opcode)

        if self.sound_timer > 0:
            if self.sound_timer == 1:
                print("SOUND BAJJA !!")
            self.sound_timer -= 1
        
        if self.delay_timer > 0:
            self.delay_timer -= 1

    def Decode_Execute(self,opcode):
        ''' Decoding the following opcode into all of the nibbles'''
        # FIX: Corrected operator precedence with parentheses
        X = (opcode & 0x0F00) >> 8
        Y = (opcode & 0x00F0) >> 4
        N = opcode & 0x000F
        NN = opcode & 0x00FF
        NNN = opcode & 0x0FFF
        
        # Moving the coundter 
        self.pc += 2
        first_nibble = opcode & 0xF000

        # Execution Begins
        if first_nibble == 0x0000:
            if NN == 0x00E0:
                # Clearing the Screen 
                self.gfx = [0]*(64*32)
                self.draw_flag = True

            elif NN == 0x00EE:
                # Returning After Resolving a subroutine 
                self.sp -= 1  # !! this might cause a problem !!!! May be not 
                self.pc = self.stack[self.sp]

        elif first_nibble == 0x1000:
            # Jumping the programm to the NNN address 
            self.pc = NNN
        
        elif first_nibble == 0x2000:
            # Starting a subroutine form address NNN
            self.stack[self.sp] = self.pc 
            self.sp += 1
            self.pc = NNN

        elif first_nibble == 0x3000:
            # Skeip if Register vX is equal to NN
            if self.v[X] == NN:
                self.pc += 2
        
        elif first_nibble == 0x4000:
            # Tf why those goonners have 2 different condition of else logic (DO SOME SEARCH)
            if self.v[X] != NN:
                self.pc += 2
        
        elif first_nibble == 0x5000:
            # If value of Vx is equal to Vy then skip 
            if self.v[X] == self.v[Y]:
                self.pc += 2

        elif first_nibble == 0x6000:
            # store the number in Vx
            self.v[X] = NN

        elif first_nibble == 0x7000:
            # Add NN to Vx register 
            # FIX: Added 8-bit wrap around
            self.v[X] = (self.v[X] + NN) & 0xFF

        elif first_nibble == 0x8000:
            last_nibble = N
            if last_nibble == 0 :
                self.v[X] = self.v[Y]
        # Some logical operations are about to begin
            elif last_nibble == 1:
                self.v[X] = self.v[X] | self.v[Y]
            elif last_nibble == 2 :
                self.v[X] = self.v[X] & self.v[Y]
            elif last_nibble == 3 :
                self.v[X] = self.v[X] ^ self.v[Y]
            elif last_nibble == 4 :
                # Do summ and generate caryy if there is any 
                sum_val = self.v[X] + self.v[Y]
                if sum_val > 255:
                    self.v[0xF] = 1 
                else :
                    self.v[0xF] = 0
                self.v[X] = sum_val & 0xFF
            elif last_nibble == 5 :
                if self.v[X] > self.v[Y]:
                    self.v[0xF] = 1 
                else :
                    self.v[0xF] = 0
                self.v[X] = (self.v[X] - self.v[Y]) & 0xFF # FIX: 8-bit wrap
            elif last_nibble == 6:
                self.v[0xF] = self.v[X] & 0x1
                self.v[X] >>= 1
            elif last_nibble == 7 :
                self.v[0xF] = 1 if self.v[Y] > self.v[X] else 0
                self.v[X] = (self.v[Y] - self.v[X]) & 0xFF
            elif last_nibble == 0xE:
                self.v[0xF] = (self.v[X] & 0x80) >> 7
                self.v[X] = (self.v[X] << 1) & 0xFF

        elif first_nibble == 0x9000:
            if self.v[X] != self.v[Y]:
                self.pc += 2
        
        elif first_nibble == 0xA000:
            self.I = NNN
        elif first_nibble == 0xB000:
            self.pc = NNN + self.v[0]
        elif first_nibble == 0xC000:
            self.v[X] = random.randint(0, 255) & NN

        elif first_nibble == 0xD000:
            # Set collision flag to zero 
            self.v[0xF] = 0 
            # Get Coordinates form Vx and Vy 
            x_ = self.v[X]
            y_ = self.v[Y]
            height = N

            # FIX: Loop was iterating y_ times instead of height
            for y_line in range(height):
                pixel_r = self.memory[self.I + y_line]
                for x_line in range(8):
                    # width is fixed for 8 pixels
                    if (pixel_r & (0x80 >> x_line)) != 0:
                        d_x = (x_ + x_line) % 64
                        d_y = (y_ + y_line) % 32
                        # FIX: Corrected index calculation from `d_x (d_y*64)` to `d_x + (d_y*64)`
                        index = d_x + (d_y * 64)
                        if self.gfx[index] == 1:
                            # if the pixel is already one then there must be a collision
                            # turn on the collision flag 
                            self.v[0xF] = 1 
                        self.gfx[index] ^= 1
            self.draw_flag = True

        elif first_nibble == 0xE000:
            last_byte = opcode & 0x00FF
            if last_byte == 0x009E:
                if self.key[self.v[X]] != 0:
                    self.pc += 2
            elif last_byte == 0x00A1:
                if self.key[self.v[X]] == 0 :
                    self.pc += 2
        
        # FIX: Corrected condition from `0x000F` to `0xF000`
        elif first_nibble == 0xF000:
            last_byte = opcode & 0x00FF
            if last_byte == 0x0007:
                self.v[X] = self.delay_timer
            elif last_byte == 0x000A:
                key_pressed = False
                for i in range(16):
                    if self.key[i] != 0:
                        self.v[X] = i
                        key_pressed = True
                        break # FIX: Added break to stop after one key
                # If no key was pressed, repeat this instruction by decrementing PC
                if not key_pressed:
                    self.pc -= 2
            
            elif last_byte == 0x0015:
                self.delay_timer = self.v[X]
            
            elif last_byte == 0x0018:
                self.sound_timer = self.v[X]
            
            elif last_byte == 0x001E:
                self.I += self.v[X]

            elif last_byte == 0x0029:
                self.I = (self.v[X] * 5) + 0x50 # FIX: Start of fontset is 0x50
            
            elif last_byte == 0x0033:
                val = self.v[X]
                self.memory[self.I] = val // 100
                self.memory[self.I + 1] = (val // 10) % 10
                self.memory[self.I + 2] = val % 10
            
            elif last_byte == 0x0055:
                for i in range (X + 1):
                    self.memory[self.I + i] = self.v[i]
            
            elif last_byte == 0x0065:
                for i in range(X + 1):
                    self.v[i] = self.memory[self.I + i]
        
        else:
            print(f"Given Oppcode is invalid: {opcode:04X}")
