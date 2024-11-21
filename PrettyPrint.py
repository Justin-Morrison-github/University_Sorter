from colorama import Fore
from pathlib import Path
from ANSI import ANSI

def main():
    src_folder_path = Path("C:\\Users\\morri\\Downloads")
    word = prompt_user_for_input()
    files = get_files_containing_word(src_folder_path, word)
    for file in files:
        pretty_path(file)


def pretty_path(file: Path):
    colors = [Fore.BLUE, Fore.GREEN, Fore.YELLOW, Fore.RED, Fore.MAGENTA, Fore.BLACK]
    folders = file.parts[3:]
    for i, x in enumerate(folders):
        if x == file.name:
            print(f"{Fore.WHITE}{x}{Fore.RESET}")
        else:
            print(f"{colors[i%5]}{x}", end = f"{ANSI.STRAIGHT_ARROW}")

def prompt_user_for_input() -> str:
    while True:
        check = input("Enter common word in file name: ")

        if check.lower() == 'q':
            print("Quit Program")
            exit()
        else:
            print()
            return check


def get_files_containing_word2(src_folder_path: Path, word:str) -> list[dict]:
    files_to_be_sent = []

    for file in src_folder_path.iterdir():
        if word.lower() in file.name.lower():
            files_to_be_sent.append(file)
        elif file.is_dir():
            files_to_be_sent += get_files_containing_word2(file, word)

    return files_to_be_sent


def get_files_containing_word(src_folder_path: Path, word: str, include_suffix:bool = False, include_folders:bool = False) -> list[dict]:
    files_to_be_sent = []

    for file in src_folder_path.iterdir():
        
        is_dir = file.is_dir()
        name_contains_word = word.lower() in file.name.lower()
        stem_contains_word = word.lower() in file.stem.lower()

        # Determine if the file or folder matches the word criteria
        matches = name_contains_word if include_suffix else stem_contains_word

        # Add directories if include_folders is True
        if is_dir and include_folders and matches:
            files_to_be_sent.append(file)

        # Add files if they are not directories
        if not is_dir and matches:
            files_to_be_sent.append(file)

        # Recursively process subdirectories
        if is_dir:
            files_to_be_sent += get_files_containing_word(file, word, include_suffix, include_folders)


    return files_to_be_sent

if __name__ == '__main__':
    main()
