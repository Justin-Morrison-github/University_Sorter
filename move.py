import os
import shutil
from colorama import Fore
import sys
from pathlib import Path
from Symbols import Symbol


def send_file(src, dst, send_enabled=False) -> None:
    """
    Sends a file from src to dst. Prints out certain results
    """

    try:
        if os.path.exists(dst):
            print(Fore.GREEN + f'\u2705 From:  {src}')
            print(Fore.RED + f'\u274C   To:  {dst}')
            print(Fore.YELLOW + f"WARNING: File Already Exists")
        else:
            if send_enabled:
                shutil.move(src, dst)
            print(Fore.GREEN + f'\u2705 From:  {src}')
            print(Fore.GREEN + f'\u2705   To:  {dst}', end="")

    except FileNotFoundError as e:
        print(Fore.YELLOW + f'\u274C From:  {src}')
        print(Fore.YELLOW + f'\u274C   To:  {dst}')
        print(Fore.RED + f"ERROR: File Not Found {e}")

    except Exception as error:
        print(error)

    print(Fore.RESET + "\n")


def user_continues(prompt="Send these files?", dst="") -> bool:
    """
    Prompts the user if they want to send files
    """
    while True:
        if dst == "":
            choice = input(f"\n{prompt} (y/n): ").strip().lower()
        else:
            choice = input(f"\n{prompt} to {dst}? (y/n): ").strip().lower()

        if choice == 'y':
            print()
            return True
        elif choice == 'n':
            print("No Files Sent")
            return False
        else:
            print("Invalid Input")


def pretty_print_substring(str: str, substr: str, start="\u2794  ", end="", color=Fore.YELLOW):
    str_len = len(str)
    substr_len = len(substr)

    index = str.lower().find(substr.lower())

    string = start + str[0: index] + color + str[index: index + substr_len] + Fore.RESET + str[index +
                                                                                               substr_len: str_len] + end
    print(string)


def return_pretty_print_string(str: str, substr: str, start="\u2794  ", end="", color=Fore.YELLOW):
    str_len = len(str)
    substr_len = len(substr)

    index = str.lower().find(substr.lower())

    string = start + str[0: index] + color + str[index: index + substr_len] + Fore.RESET + str[index +
                                                                                               substr_len: str_len] + end
    return string


def pretty_path(file: str, basepath: str):

    colors = [Fore.BLUE, Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.MAGENTA, Fore.BLACK]

    folders = file["src"].split("\\")
    index = folders.index(os.path.basename(basepath)) + 1
    for i in range(index, len(folders)):
        if i == len(folders) - 1:
            print(Fore.WHITE + folders[i])
        else:
            print(colors[i-index] + folders[i], end=" -> ")
    print(Fore.RESET, end="")


def prompt_user(prompt: str, exit_char='q') -> str:
    while True:
        keyword = input(prompt)

        if keyword.lower() == exit_char:
            print("Quit Program")
            exit()
        else:
            return keyword


def replace_previous_print(string):
    sys.stdout.write("\033[F")  # back to previous line
    sys.stdout.write("\033[K")  # clear line
    print(string)


def print_hierarchy(
        src_folder_path: str, depth=0, arrow_color=Fore.BLACK, count_color=Fore.BLACK, file_color=Fore.CYAN,
        size_color=Fore.GREEN, show_arrow=True, show_count=True, indent="\t", deci_places=2):
    depth += 1
    count = 0
    file_list = os.listdir(src_folder_path)
    for file in file_list:
        path = os.path.join(src_folder_path, file)
        if os.path.isdir(path):
            print(f"{indent * (depth-1)}", end=" ")

            if (show_arrow):
                print(f"{arrow_color}{Symbol.ARROW}{Fore.RESET}", end=" ")

            count += 1
            if (show_count):
                print(f"{count_color}{count:03d}{Fore.RESET}", end=" ")

            print(f'{file_color}{file}{Fore.RESET}', end="")

            size = get_folder_size(path)
            print(f"{size_color}{size: .{deci_places}f}{Fore.RESET}"),

            print_hierarchy(path, depth, arrow_color, count_color, file_color,
                            size_color, show_arrow, show_count, indent, deci_places)


def get_folder_size(folder):
    return ByteSize(sum(file.stat().st_size for file in Path(folder).rglob('*')))


class ByteSize(int):
    _KB = 1024
    _suffixes = 'B', 'KB', 'MB', 'GB', 'PB'

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.bytes = self.B = int(self)
        self.kilobytes = self.KB = self / self._KB**1
        self.megabytes = self.MB = self / self._KB**2
        self.gigabytes = self.GB = self / self._KB**3
        self.petabytes = self.PB = self / self._KB**4
        * suffixes, last = self._suffixes
        suffix = next((
            suffix
            for suffix in suffixes
            if 1 < getattr(self, suffix) < self._KB
        ), last)
        self.readable = suffix, getattr(self, suffix)

        super().__init__()

    def __str__(self):
        return self.__format__('.2f')

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, super().__repr__())

    def __format__(self, format_spec):
        suffix, val = self.readable
        return '{val:{fmt}} {suf}'.format(val=val, fmt=format_spec, suf=suffix)

    def __sub__(self, other):
        return self.__class__(super().__sub__(other))

    def __add__(self, other):
        return self.__class__(super().__add__(other))

    def __mul__(self, other):
        return self.__class__(super().__mul__(other))

    def __rsub__(self, other):
        return self.__class__(super().__sub__(other))

    def __radd__(self, other):
        return self.__class__(super().__add__(other))

    def __rmul__(self, other):
        return self.__class__(super().__rmul__(other))


# def __init__():
#     pass
