
import re
import time
from typing import Iterable
from colorama import Fore
import sys
from pathlib import Path
from ANSI import ANSI
import time
from typing import Iterable, Any
from enum import StrEnum, auto


def replace_previous_line(string):
    sys.stdout.write("\033[F")  # back to previous line
    sys.stdout.write("\033[K")  # clear line
    print(string)


def clear_n_previous_lines(n):
    for _ in range(n):
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
        time.sleep(0.05)


def print_n_lines_back(n: int, string: str):
    for _ in range(n):
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
        time.sleep(0.05)
    print(string)


def prompt_user(prompt: str, exit_char='q') -> str:
    while True:
        keyword = input(prompt)

        if keyword.lower() == exit_char:
            print("Quit Program")
            exit()
        else:
            return keyword


def user_continues_with_dst_option(prompt="Send these files?", dst="") -> bool:
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


def user_choice_bool(prompt="Send these files? (y/n): ") -> bool:
    """
    Prompts the user if they want to prompt. Accepts Y/y or N/n
    """
    while True:
        try:
            choice = input(f"\n{prompt}").strip().lower()

            if choice == 'y':
                return True
            elif choice == 'n':
                return False
            else:
                print("Invalid Input")

        except KeyboardInterrupt:
            raise KeyboardInterrupt
            # return None


def user_choice_numbered(args: Iterable[Any],
                         input_prompt="Enter Option: ", option_prompt="Options: ", delete_lines:bool = True) -> Any | None:
    """
    Prompts the user if to select an item from an iterable of items. 
    If exit_option True, then if input is the exit_char, will return None.
    Keyboard Interupts will also return None.
    """

    print(f"\n{option_prompt}")
    count = 1
    for elem in args:
        print(f"    {count}.  {str(elem).title()}")
        count += 1

    while True:
        try:
            choice = int(input(f"\n{input_prompt}").strip().lower())

        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            choice = -1

        if (choice - 1) in range(0, len(args)):
            clear_n_previous_lines(count + 2)
            return args[choice - 1]
        else:
            print("Invalid Input")
