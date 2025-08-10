from def_memory import *


class Chip8():
    def __init__(self):
        self.pc =reg_pc
        self.opcode = opcode
        self.I = reg_index
        self.sp = reg_stackPointer
        self.memory = memory
        self.chipfontset = [1,12]



    def reset(self):
        self.pc = 0x200
        self.opcode = 0 
        self.I=0
        self.sp=0
        # todos :  Clear display	
        # todos :  Clear stack
        #  todos : Clear registers V0-VF
        # todos :  Clear memory
        # todos : loading fontset 
        for i in range(80):
            memory[i]=self.chipfontset[i]
        # todos :  reset timers
    
    def emulateCycle(self):
        ''' Now the actual fun begines FED cycle reading first 45 bits of 
            the program finding the means the opcode and perfroming the 
            instruction given in the opcode'''
        

        

    def loadRom(self,path):
        ''' Load the file for the given path or file name then store the program form 
            memory address 0x200 (512) onward just iterating on the file and storing 
            the data in memory '''
        
        rom_data = open(path)
        for i in range(len(rom_data)):
            memory[i+512] = rom_data[i]
        



    def emulateCycle():
        ''' This Function will trigger the Fetch, Decode and Execute operation of 
            one opcode which is specified by the address form the PC, since the Chip8
            has the opcode of 2 bytes so we will run it FDE cycle twiced '''
        pass


