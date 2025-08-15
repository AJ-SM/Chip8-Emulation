
import sys 

from modules.core import Chip8
from modules.renderer import draw_to_console
import time 

def main():


    rom_path = r"D:\CLEAN_CODE\Projects\Chip8Emu\Chip8-Emulation\roms\15 Puzzle [Roger Ivie].ch8"

    # Initialize the Chip8 system
    chip8 = Chip8()
    chip8.loadRom(rom_path)



    print(f"Starting emulation of '{rom_path}'. Press Ctrl+C to exit.")
    
    while True:
        try:
            # Emulate one cycle
            chip8.emulateCycle()

            # If the draw flag is set, render the screen
            if chip8.draw_flag:
                draw_to_console(chip8.gfx)
                chip8.draw_flag = False

            # Sleep to slow down emulation speed for visibility
            # A value of ~0.002 simulates a reasonable CPU speed.
            time.sleep(0.002) 

        except KeyboardInterrupt:
            print("\nEmulation stopped.")
            break
        except Exception as e:
            print(f"\nAn error occurred during emulation: {e}")
            break


if __name__ == "__main__":
    main()
