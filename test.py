# import numpy as np 
# b = np.uint8(5)
# opcode =0xA2F0
# var = hex(opcode & 0xF000)

# if(var == hex(0xa000)):
#     h = opcode & 0x0FFF
# print(hex(h))    

path = r"D:\CLEAN_CODE\Projects\Chip8Emu\Chip8-Emulation\roms\15 Puzzle [Roger Ivie].ch8"
print(open(path, "rb").read())
