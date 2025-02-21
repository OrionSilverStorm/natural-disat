RED = "\033[101m"
GREEN = "\033[102m"
YELLOW = "\033[103m"
BLUE = "\033[104m"
MAGENTA = "\033[105m"
CYAN = "\033[106m"

def RGB(r: int, g: int, b: int):
    # sets foreground colour to RGB values
    return f"\033[48;2;{r};{g};{b}m"