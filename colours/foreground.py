BLACK = "\033[30m"
GREY = "\033[90m"
WHITE = "\033[97m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"


def RGB(r: int, g: int, b: int):
    # sets foreground colour to RGB values
    return f"\033[38;2;{r};{g};{b}m"