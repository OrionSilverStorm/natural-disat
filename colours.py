# ANSI escape codes to change the colour
# https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit

END = "\033[0m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"

def fgRGB(r: int, g: int, b: int):
    # sets foreground colour to RGB values
    return f"\033[38;2;{r};{g};{b}m"

def bgRGB(r: int, g: int, b: int):
    # sets foreground colour to RGB values
    return f"\033[48;2;{r};{g};{b}m"

print(f"{RED}red {GREEN}green {YELLOW}yellow {BLUE}blue {MAGENTA}magenta {CYAN}cyan {END}")
print(f"{fgRGB(128,50,76)}{bgRGB(12,37,58)}Hiiii{END}")