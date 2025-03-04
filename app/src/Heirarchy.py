from pathlib import Path
import tkinter
from tkinter import filedialog
from sys import argv
from colorama import Fore
from ANSI import ANSI

def main():
    init_dir = "C:\\Users\\morri\\Downloads"

    if len(argv) == 1:  # No folder given
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        folder = Path(filedialog.askdirectory(initialdir=init_dir))
        print(Fore.YELLOW + f"\n{folder.stem}" + Fore.RESET, get_folder_size(folder))

        print_hierarchy(folder)

    else:  # Folder given
        print("Error")
        return 1

def print_hierarchy(
        src_folder_path: str, depth=0, arrow_color=Fore.WHITE, count_color=Fore.WHITE, file_color=Fore.CYAN,
        size_color=Fore.GREEN, show_arrow=True, show_count=True, indent="\t", deci_places=2):
    depth += 1
    count = 0
    for file in Path(src_folder_path).iterdir():
        path = Path(src_folder_path) / Path(file).name
        if path.is_dir():
            print(f"{indent * (depth-1)}", end=" ")

            if (show_arrow):
                print(f"{arrow_color}{ANSI.ARROW}{Fore.RESET}", end=" ")

            count += 1
            if (show_count):
                print(f"{count_color}{count:03d}{Fore.RESET}", end=" ")

            print(f'{file_color}{file.name}{Fore.RESET}', end="")

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

if __name__ == '__main__':
    main()
