


def draw_to_console(gfx_buffer):
    """A simple function to render the graphics buffer to the console."""
    print("+" + "-" * 64 + "+")
    for y in range(32):
        line = "|"
        for x in range(64):
            if gfx_buffer[x + y * 64]:
                line += '█'
            else:
                line += ' '
        line += "|"
        print(line)
    print("+" + "-" * 64 + "+")
