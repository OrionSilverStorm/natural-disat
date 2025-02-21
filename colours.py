class fg:
    # changes colour of the text (foreground)
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

class bg:
    # changes colour of the background
    BLACK = "\033[40m"
    GREY = "\033[100m"
    WHITE = "\033[107m"

    RED = "\033[101m"
    GREEN = "\033[102m"
    YELLOW = "\033[103m"
    BLUE = "\033[104m"
    MAGENTA = "\033[105m"
    CYAN = "\033[106m"

    def RGB(r: int, g: int, b: int):
        # sets background colour to RGB values
        return f"\033[48;2;{r};{g};{b}m"

class style:
    BOLD = "\033[1m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    DOUBLEUNDERLINE = "\033[21m"
    OVERLINE = "\033[53m"
    INVERT = "\033[7m"
    STRIKETHROUGH = "\033[9m"

END = "\033[0m"