from pathlib import Path
from enum import IntEnum, StrEnum, auto
import sys
import time
from move import user_continues
from colorama import Fore
import json
from ANSI import ANSI
from Settings import Settings
from typing import Optional


class Style(StrEnum):
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    INDENT = "     "


class Color(StrEnum):
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    SUCCESS = Fore.GREEN


class Mode(StrEnum):
    DEBUG = auto()
    SEND = auto()


class Folders(StrEnum):
    ASSIGNMENT = "Assignment"
    INFO = "Info"
    LAB = "Lab"
    LECTURE = "Lecture"
    PASS = "Pass"
    PRACTICE = "Practice"
    REVIEW = "Review"
    TEXTBOOK = "Textbook"
    TUTORIAL = "Tutorial"
    WOOCLAP = "Wooclap"

    DOWNLOADS = "Downloads"
    UNIVERSITY = "University"


class Packet():

    SUCCESS = 0

    class Error(IntEnum):
        SRC_DNE = 1
        DST_DNE = 2
        DST_PARENT_DNE = 3
        DST_ALREADY_EXISTS = 4

    class OP(IntEnum):
        PRINT = 0
        SAFE_SEND = 1
        FULL_SEND = 2

    def __init__(self, src: Path, dst: Path, course_code: str, course_name: str, folder_type: Folders,
                 file_number: int = None):
        self.src = src
        self.dst = dst
        self.course_code = course_code
        self.name = self.src.stem
        self.course_name = course_name
        self.file_number = file_number
        self.folder_type = folder_type

        for from_folder in [Folders.DOWNLOADS, Folders.UNIVERSITY]:
            if from_folder in src.parts:
                self.From = from_folder
                break

    def str_directories_between(self, target: Path):
        num_between = target.parts.index(target.parent.name) - target.parts.index(self.course_name)
        if num_between == 0:
            return ""

        return f"/{'.' * num_between}/"

    def __str__(self):

        if self.From == Folders.UNIVERSITY:
            src_path = f"{self.course_name}{self.str_directories_between(self.src)}{self.src.parent.name if self.src.parent.name != self.course_name else ''}/{self.src.name}"
            dst_path = f"{self.course_name}{self.str_directories_between(self.dst)}{self.dst.parent.name if self.dst.parent.name != self.course_name else ''}/{self.dst.name}"

        else:
            src_path = f"{self.src.parent.name if self.src.parent.name != self.course_name else ''}/{self.src.name}"
            dst_path = '/'.join(x for x in self.dst.parts[self.dst.parts.index(self.course_name):])

        return (
            f"     {ANSI.ARROW} SRC:  {src_path}\n"
            f"     {ANSI.ARROW} DST:  {dst_path}\n"
            + (
                f"     {Fore.YELLOW}   {ANSI.WARNING} WARNING (Folder Does Not Exist):  {Style.UNDERLINE}{self.dst.parent.name}{Style.RESET} \n{Fore.RESET}"
                if not self.dst.parent.exists() else ""
            )
        )

    def __repr__(self):
        return f"(src: {self.src.parent.name}/{self.src.name}, dst: {self.dst.parent.name}/{self.dst.name})"

    def send(self, mode: Mode = Mode.DEBUG) -> None:
        """
        Sends a packet from self.src to self.dst. Prints out success, failure, or warnings.
        Returns 0 (Packet Success) on success, else returns defined Packet Error value.
        """
        mode_str = f"{Fore.LIGHTMAGENTA_EX}(DEBUG)" if mode == Mode.DEBUG else ""
        if self.dst.exists():
            print(f"{Style.INDENT}{Fore.GREEN}{ANSI.SUCCESS} SRC:  {self.src}")
            print(f"{Style.INDENT}{Fore.YELLOW}{ANSI.FAILURE} DST:  {self.dst}")
            print(f"{Style.INDENT}{Fore.YELLOW}WARNING: DST File Already Exists\n")
            return Packet.Error.DST_ALREADY_EXISTS

        elif not self.dst.parent.exists():
            print(f"{Style.INDENT}{mode_str}{Fore.GREEN}{ANSI.SUCCESS} SRC:  {self.src}")
            print(f"{Style.INDENT}{mode_str}{Fore.YELLOW}{ANSI.WARNING} DST:  {self.dst}")
            print(f"{Style.INDENT}{mode_str}{Fore.YELLOW}{ANSI.WARNING} WARNING (Folder Does Not Exist): {Style.UNDERLINE}{self.dst.parent.name}{Style.RESET}\n")
            return Packet.Error.DST_PARENT_DNE

        elif not self.src.exists():
            print(f"{Style.INDENT}{mode_str}{Fore.YELLOW}{ANSI.WARNING} SRC:  {self.src}")
            print(f"{Style.INDENT}{mode_str}{Fore.GREEN}{ANSI.SUCCESS} DST:  {self.dst}")
            print(f"{Style.INDENT}{mode_str}{Fore.YELLOW}{ANSI.WARNING} WARNING (Src file Does Not Exist): {Style.UNDERLINE}{self.src.name}{Style.RESET}\n")
            return Packet.Error.SRC_DNE

        else:
            try:
                if mode == Mode.SEND:
                    self.src.rename(self.dst)

                print(f"{Style.INDENT}{mode_str}{Fore.GREEN}{ANSI.SUCCESS} SRC:  {self.src}")
                print(f"{Style.INDENT}{mode_str}{Fore.GREEN}{ANSI.SUCCESS} DST:  {self.dst}{Fore.RESET}\n")
                return Packet.Error.DST_ALREADY_EXISTS

            except FileNotFoundError as e:
                print(f"{Fore.RED}ERROR: {e}{Fore.RESET}")
                # outcome = f"{Fore.GREEN}{ANSI.SUCCESS}" if self.src.exists() else f"{Fore.RED}{ANSI.FAILURE}"
                # print(f"{Style.INDENT}{mode_str}{outcome} SRC:  {self.src}")
                # print(f"{Style.INDENT}{mode_str}{Fore.RED}{ANSI.FAILURE} DST:  {self.dst}")
                # print(f"{Style.INDENT}{mode_str}{Fore.RED}{e}")
                # return Packet.Error.SRC_DNE

        print(Fore.RESET + "\n")


def main():
    file = Path(__file__).stem

    settings = Settings("JSON/settings.json", file)

    with open(settings.json_file, 'r') as json_file:
        course_data: dict = json.load(json_file)

    class_paths = create_class_dict(course_data, settings.basepath)

    folders_to_be_made: set[Path] = set()

    packets_to_be_sent = traverse_folder_packet(settings.src_path, class_paths, course_data, folders_to_be_made)

    try:
        if len(packets_to_be_sent) == 0:
            print("No files found...")
        else:
            mode = user_select_operation_mode()
            print(f"{Fore.MAGENTA if mode == Mode.DEBUG else Fore.GREEN}{mode.upper()} MODE {Fore.RESET}")

            process_packets(packets_to_be_sent, Packet.OP.PRINT)
            if user_continues():
                if user_wants_folder_creation(folders_to_be_made):
                    process_packets(packets_to_be_sent, Packet.OP.FULL_SEND, mode)
                else:
                    process_packets(packets_to_be_sent, Packet.OP.SAFE_SEND, mode)

    except KeyboardInterrupt:
        print("\nProgram Exited")
        return

    print(Fore.RESET)


def user_wants_folder_creation(folders_to_be_made) -> bool:
    """
    Prompts the user if they want to create folders that don't exist (if any)
    in order to send the files.
    """
    if len(folders_to_be_made) == 0:
        return True

    while True:
        choice = input("Create Missing Folders? (y/n): ").strip().lower()

        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid Input")


def user_select_operation_mode() -> Mode:
    """
    Prompts the user to pick what operation mode to use.
    Returns selected Mode.
    """
    print("\nOperation Modes:")
    print("  1.  SEND")
    print("  2.  DEBUG\n")
    count = 4

    while True:
        count += 1
        try:
            choice = int(input("Enter Mode: "))
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            choice = 0

        if choice == 1:
            clear_n_previous_lines(count)
            return Mode.SEND
        elif choice == 2:
            clear_n_previous_lines(count)
            return Mode.DEBUG
        else:
            print("Invalid Input")


def clear_n_previous_lines(n):
    for _ in range(n):
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")  # clear line
        time.sleep(0.05)


def validate_path(path: Path) -> None:
    """Raise an error if the given path doesn't exist."""
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")


def create_class_dict(university: dict, basepath: Path) -> dict:
    classes = {}
    for year, semesters in university.items():
        for semester, class_list in semesters.items():
            folder_path: Path = basepath / year / semester
            class_paths: Path = get_class_paths(folder_path)
            classes.update(dict(zip(class_list, class_paths)))

    return classes


def get_class_paths(folder_path: Path):
    class_paths = []
    for folder in folder_path.iterdir():
        path: Path = folder_path / folder
        if path.is_dir():
            class_paths.append(path)

    return class_paths


def process_packets(packet_list: list[Packet], command=Packet.OP.PRINT, mode=Mode.DEBUG, recursive_call=False):
    mode_str = f"{Fore.LIGHTMAGENTA_EX}(DEBUG){Fore.RESET}" if mode == Mode.DEBUG else ""

    action = f"{mode_str}Files to be sent" if command == Packet.OP.PRINT else f"{mode_str}Sending"
    if not recursive_call:
        print(f"\n{action}:")

    last_course_code = ""
    last_folder_type = ""

    for packet in packet_list:

        if packet.src.is_dir() and recursive_call == False:
            x = [Packet(file, packet.dst.parent / file.name, packet.course_code,
                        packet.course_name, packet.folder_type, packet.file_number) for file in packet.src.iterdir()]

            process_packets(x, command, mode, True)
            continue

        if packet.course_code != last_course_code:
            print(f"{Fore.LIGHTCYAN_EX}{packet.course_code}: {packet.course_name}{Fore.RESET}")
            last_course_code = packet.course_code
            time.sleep(0.05)

        if packet.folder_type != last_folder_type:
            print(f"{Fore.BLUE}  {packet.folder_type}{Fore.RESET}")
            last_folder_type = packet.folder_type
            time.sleep(0.05)

        if command == Packet.OP.PRINT:
            print(packet)

        elif command == Packet.OP.FULL_SEND or command == Packet.OP.SAFE_SEND:
            if command == Packet.OP.FULL_SEND and not packet.dst.parent.exists():
                if mode == Mode.SEND:
                    packet.dst.parent.mkdir()

                print(f'{Style.INDENT}{mode_str}{Fore.YELLOW}{ANSI.ARROW} \"{packet.dst.parent.name}\" Folder Created in \"{packet.dst.parent.parent.parent.name}\\{packet.dst.parent.parent.name}\"{Fore.RESET}')

            packet.send(mode)

        time.sleep(0.05)


# TODO Remove Class Code from folder when being added (Lab/SYSC 2320 Lab 5 ---> Lab/Lab 5)

def find_or_create_folder(parent: Path, folder_name: str, folders_to_be_made: set[Path]) -> Optional[str]:
    """Search for a folder matching the target name in the parent directory."""

    if not parent.exists():
        parent = find_or_create_folder(parent.parent, folder_name.split()[0], folders_to_be_made)

    for folder in parent.glob(f"*{folder_name}*"):
        if folder.is_dir():
            return folder

    new_folder = parent / folder_name
    if not new_folder.exists():
        folders_to_be_made.add(new_folder)

    return new_folder


def find_path_within_parent(parent: Path, file: Path, folder: Folders, folders_to_be_made: set[Path]):

    # If there is a number associated with folder (e.g., "Assignment 5")
    if folder in [Folders.ASSIGNMENT, Folders.LAB, Folders.LECTURE, Folders.TUTORIAL]:

        try:
            split_stem = file.stem.lower().split()
            index = split_stem.index(folder.lower())

            # Ensure there's a file number following the folder keyword (e.g., "Assignment 5")
            file_number = int(split_stem[index + 1])
            target_folder = f'{folder} {file_number}'

        except ValueError:
            raise ValueError(f"'{folder}' not found in the destination stem: {file.stem}")

        except (IndexError, ValueError):
            raise ValueError(f"Expected a file number after '{folder}' in the stem: {file.stem}")

        # Update the destination path
        matching_folder_path = find_or_create_folder(parent / folder, target_folder, folders_to_be_made)

    elif folder in [Folders.INFO, Folders.REVIEW, Folders.PASS, Folders.TEXTBOOK, Folders.WOOCLAP]:
        matching_folder_path = find_or_create_folder(file.parent, folder, folders_to_be_made)
    else:
        return parent / file

    return matching_folder_path / file.name


def traverse_folder_packet(
        src_folder_path: Path, class_paths: dict, course_data: dict, folders_to_be_made: list[Path]) -> list[Packet]:
    files_to_be_sent = []

    for file in src_folder_path.iterdir():
        tag = file.name[:9].replace(" ", "").replace("-", "").replace("_", "").upper().strip()

        if tag in class_paths:
            parent_path: Path = class_paths[tag]
            course_name = parent_path.name

            dst: Path = parent_path / file.name
            for folder in [
                    Folders[folder]
                    for folder in course_data[parent_path.parent.parent.name][parent_path.parent.name][tag]["folders"]]:

                if folder in file.stem:
                    dst = find_path_within_parent(parent_path, file, folder, folders_to_be_made)
                    break

            packet = Packet(file, dst, tag, course_name, folder)
            files_to_be_sent.append(packet)

        elif file.is_dir():
            files_to_be_sent += traverse_folder_packet(file, class_paths, course_data, folders_to_be_made)

    return files_to_be_sent


if __name__ == "__main__":
    main()
