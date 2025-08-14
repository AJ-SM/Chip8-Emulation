from def_memory import *
import random

class Chip8():
    def __init__(self):
        self.pc =reg_pc
        self.opcode = opcode
        self.I = reg_index
        self.sp = reg_stackPointer
        self.memory = memory
        self.stack = stack
        self.v = bytearray(16) # TODO Do type checking before uploading 
        # self.chipfontset = [1,12]
        # also including timers
        self.sound_timer = reg_soundTimer
        self.delay_timer = reg_delayTimer
        # Dont Want to poplulate these all over the palce 
        self.screen = [0] * (64*32)
        self.draw_flag =False
        self.key = [0] * 16 



    def reset(self):
        self.pc = hex(0x200)
        self.opcode = 0 
        self.I=0
        self.sp=0
        # todos :  Clear display	
        # todos :  Clear stack
        #  todos : Clear registers V0-VF
        # todos :  Clear memory
        # todos : loading fontset 
        for i in range(80):
            self.memory[i]=self.chipfontset[i]
        # todos :  reset timers
    
    def emulateCycle(self):
        ''' Now the actual fun begines FED cycle reading first 45 bits of 
            the program finding the means the opcode and perfroming the 
            instruction given in the opcode'''
    
    
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
        
        # loading the font into memory for location 0x000
        for i in range(len(fontset)):
            self.memory[i]=fontset[i]
    
        

        

    def loadRom(self,path):
        ''' Load the file for the given path or file name then store the program form 
            memory address 0x200 (512) onward just iterating on the file and storing 
            the data in memory '''
        
        self.rom_data = open(path)
        for i in range(len(self.rom_data)):
            self.memory[i+512] = self.rom_data[i]
        



    def emulateCycle(self,pc):
        ''' This Function will trigger the Fetch, Decode and Execute operation of 
            one opcode which is specified by the address form the PC, since the Chip8
            has the opcode of 2 bytes so we will run it FDE cycle twiced '''
        
        # Feteching the opcode and create 16 bit form  2 * 8 bit..
        self.opcode = self.memory[pc]<<8 | self.memory[pc+1]
        self.Decode_Execute(opcode)

        if self.sound_timer >0:
            if self.sound_timer ==1:
                print("SOUND BAJJA !!")
            self.sound_timer-=1
        
        if self.delay_timer >0:
            self.delay_timer -=1


        # Decoding OpCode.. 
    
    def Decode_Execute(self,opcode):
        ''' Decoding the following opcode into all of the nibbles'''
        X = opcode & 0x0F00 >>8
        Y = opcode & 0x00F0 >>4
        N = opcode & 0x000F
        NN = opcode & 0x00FF
        NNN = opcode & 0x0FFF
        # Moving the coundter 
        self.pc +=2
        first_nibble = opcode & 0xF000

        # Execution Begins
        if first_nibble == 0x0000:
            if NN == 0x00E0:
                # Clearing the Screen 
                self.screen = [0]*(64*32)
                self.draw_flag =True    

            elif NN == 0x00EE:
                # Returning After Resolving a subroutine 
                self.sp -= 1  # !! this might cause a problem !!!! May be not 
                self.pc = self.stack[self.sp]
            else:
                pass
        elif first_nibble == 0x1000:
            # Jumping the programm to the NNN address 
            self.pc = NNN
        
        elif first_nibble == 0x2000:
            # Starting a subroutine form address NNN
            self.stack[self.sp] = self.pc 
            self.sp +=1
            self.pc = NNN
        elif first_nibble == 0x3000:
            # Skeip if Register vX is equal to NNJ
            if self.v[X] == NN:
                self.pc +=2    
        
        elif first_nibble == 0x4000:
            # Tf why those goonners have 2 different condition of else logic (DO SOME SEARCH)
            if self.v[X] != NN:
                self.pc +=2
        
        elif first_nibble == 0x5000:
            # If value of Vx is equal to Vy then skip 
            if self.v[X] == self.v[Y]:
                self.pc+=2
        elif first_nibble == 0x6000:
            # store the number in Vx
            self.v[X] = NN
        elif first_nibble == 0x7000:
            # Add NN to Vx register 
            self.v[X] += NN
        elif first_nibble == 0x8000:
            if N ==0 :
                self.v[X]=self.v[Y]
        # Some logical operations are about to begin
            elif N ==1:
                self.v[X] = self.v[X] | self.v[Y]
            elif N ==2 :
                self.v[X] = self.v[X] & self.v[Y]
            elif N==3 :
                self.v[X] = self.v[X] ^ self.v[Y]
            elif N ==4 :
                # Do summ and generate caryy if there is any 
                sum = self.v[X] + self.v[Y]
                if sum > 255:
                    self.v[0xF] = 1 
                else :
                    self.v[0xF] = 0
                self.v[X] = sum & 0xFF
            elif N ==5 :
                if self.v[X] >self.v[Y]:
                    self.v[0xF] =1 
                else :
                    self.v[0xF] = 0
                self.v[X] -= self.v[Y]
                self.v[X] & 0xFF # Potential Error 
            elif N ==6:
                self.v[0xF] = self.v[X] & 0x1
                self.v[X] >>= 1
            elif N ==7 :
                self.v[0xF] = 1 if self.v[Y] > self.v[X] else 0
                self.v[X] = (self.v[Y] - self.v[X]) & 0xFF
            elif N ==0x000E :
                self.v[0xF] = (self.v[X] & 0x80) >> 7
                self.v[X] = (self.v[X] << 1) & 0xFF
        elif first_nibble == 0x9000:
            if self.v[X] != self.v[Y]:
                self.pc +=2

        elif first_nibble == 0xA000:
            self.I = NNN
        elif first_nibble == 0xB000:
            self.pc = NNN +self.v[0]
        elif first_nibble == 0xC000:
            self.v[X] = random.randint(0, 255) & NN
        elif first_nibble == 0xD000:
            

            


        



        


