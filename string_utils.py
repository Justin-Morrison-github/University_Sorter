from colorama import Fore

UNDERLINE = "\033[4m"
RESET = "\033[0m"


def pretty_print_substring(str: str, substr: str, start="", end="", color=Fore.YELLOW):
    print(pretty_substring(str, substr, start, end, color))


def pretty_substring(str: str, substr: str, start: str = "", end="", color=Fore.YELLOW):
    str_len = len(str)
    substr_len = len(substr)

    index = str.lower().find(substr.lower())

    string = start + str[0: index] + color + str[index: index + substr_len] + Fore.RESET + str[index +
                                                                                               substr_len: str_len] + end
    return string


def underline(string: str):
    return f"{UNDERLINE}{string}{RESET}"

def color(string: str, color):
    return f"{color}{string}{Fore.RESET}"

def underline_color(string:str, color = Fore.YELLOW):
    return f"{UNDERLINE}{color}{string}{RESET}"


def prepend(string:str, start:str):
    return start + string