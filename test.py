import numpy as np 
b = np.uint8(5)
opcode =0xA2F0
var = hex(opcode & 0xF000)

if(var == hex(0xa000)):
    h = opcode & 0x0FFF
print(hex(h))    


