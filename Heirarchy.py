from pathlib import Path
import tkinter
from tkinter import filedialog
from move import get_folder_size
from sys import argv
from colorama import Fore
from ANSI import ANSI

def main():
    init_dir = "C:\\Users\\morri\\Downloads"

    if len(argv) == 1:  # No folder given
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        folder = Path(filedialog.askdirectory(initialdir=init_dir))
        print(Fore.YELLOW + f"\n{folder.stem}" + Fore.RESET, get_folder_size(folder))

        print_hierarchy(folder, arrow_color=Fore.WHITE, count_color=Fore.WHITE)

    else:  # Folder given
        print("Error")
        return 1

def print_hierarchy(
        src_folder_path: str, depth=0, arrow_color=Fore.BLACK, count_color=Fore.BLACK, file_color=Fore.CYAN,
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


if __name__ == '__main__':
    main()
