from colorama import Fore


def pretty_print_substring(str: str, substr: str, start="\u2794  ", end="", color=Fore.YELLOW):
    str_len = len(str)
    substr_len = len(substr)

    index = str.lower().find(substr.lower())

    string = start + str[0: index] + color + str[index: index + substr_len] + Fore.RESET + str[index +
                                                                                               substr_len: str_len] + end
    print(string)


def pretty_print_string(str: str, substr: str, start: str, end="", color=Fore.YELLOW):
    str_len = len(str)
    substr_len = len(substr)

    index = str.lower().find(substr.lower())

    string = start + str[0: index] + color + str[index: index + substr_len] + Fore.RESET + str[index +
                                                                                               substr_len: str_len] + end
    return string
