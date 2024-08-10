from move import prompt_user, pretty_print_substring, replace_previous_print, user_continues, send_file
import os
import tkinter
from tkinter import filedialog
from colorama import Fore
import time

SRC_COLOR = Fore.GREEN
KEYWORD_COLOR = Fore.YELLOW
DST_COLOR = Fore.CYAN


def main(send_enabled: bool):
    tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
    default_folder = "C:\\Users\\morri\\Downloads"

    # Select folder you are searching through
    src_folder = prompt_for_folder("Folder To Search: ", default_folder, 'src')

    tkinter.Tk().update_idletasks()  # This line is needed to prevent second window from hanging, would remove otherwise

    # Get key word to check
    key_word = prompt_user("Enter Key Word: ")
    print_keyword(key_word)

    # Select folder to send files to
    dst_folder = prompt_for_folder("Destination Folder: ", default_folder, 'dst')

    # Get all matching files from src_folder
    files_to_be_sent = find_files_with_keyword(src_folder, dst_folder, key_word)

    if len(files_to_be_sent) == 0:
        print_no_files_found_msg(src_folder, key_word)
    else:
        print_matching_files(src_folder, key_word, files_to_be_sent)

        # User confirm the sending of files
        dst_string = DST_COLOR + dst_folder + Fore.RESET
        if user_continues("Send these files", dst=dst_string):
            if send_enabled:
                send_files(files_to_be_sent, send_enabled)
            else:
                print("Send Function Not Enabled")


def find_files_with_keyword(src_folder: str, dst_folder: str,  check: str) -> list[dict]:
    file_list = []

    for dirpath, _, filenames in os.walk(src_folder):
        for file in filenames:
            if check.lower() in file.lower():
                file_list.append(
                    {
                        "src": os.path.join(dirpath, file),
                        "dst": os.path.join(dst_folder, file)
                    }
                )

    return file_list


def prompt_for_folder(prompt, init_dir, type) -> str:
    print(f"{prompt}", end="")
    folder = filedialog.askdirectory(initialdir=init_dir)
    if type == 'src':
        print(f"{SRC_COLOR}{folder}{Fore.RESET}")
    elif type == 'dst':
        print(f"{DST_COLOR}{folder}{Fore.RESET}")
    return folder


def print_keyword(key_word: str) -> None:
    replace_previous_print(f"Key Word: {KEYWORD_COLOR}{key_word}{Fore.RESET}")


def print_no_files_found_msg(src_folder: str, key_word: str) -> None:
    print(f"\nNo Files in {Fore.YELLOW}{src_folder}{Fore.RESET} contain: {Fore.YELLOW}{key_word}{Fore.RESET}")


def print_matching_files(src_folder: str, key_word: str, files: list[dict]) -> None:
    print(f"\nFiles In {SRC_COLOR}{src_folder}{Fore.RESET} containing {KEYWORD_COLOR}{key_word}{Fore.RESET}:")
    for index, file in enumerate(files):
        pretty_print_substring(file["src"], key_word, f'  {index:03d}  \u2794  ', color=KEYWORD_COLOR)


def send_files(files: list[dict], send_enabled) -> None:
    for file in files:
        send_file(file["src"], file["dst"], send_enabled)
        time.sleep(0.1)


if __name__ == "__main__":
    # Bool controls whether program will send files or not. Set to false for debugging
    main(False)
