import os
import tkinter
from tkinter import filedialog
from move import print_hierarchy, get_folder_size
from sys import argv
from colorama import Fore


def main():
    init_dir = "C:\\Users\\morri\\Downloads"

    if len(argv) == 1:  # No folder given
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        folder = filedialog.askdirectory(initialdir=init_dir)
        print(Fore.YELLOW + f"\n{os.path.basename(folder)}" + Fore.RESET, get_folder_size(folder))

        print_hierarchy(folder, arrow_color=Fore.WHITE, count_color=Fore.WHITE)

    else:  # Folder given
        print("Error")
        return 1


if __name__ == '__main__':
    main()
