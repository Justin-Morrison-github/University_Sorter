from pathlib import Path
from enum import IntEnum, StrEnum, auto
from colorama import Fore, init as colorama_init
import json
from Settings import Settings
from typing import Optional
from terminal_utils import user_choice_bool, user_choice_numbered, Delay, print_wait
from string_utils import underline
from exceptions import DestinationParentDoesNotExist, PathException, SourcePathDoesNotExist, DestinationPathAlreadyExists, FolderNotEmpty, DEBUG_IGNORE_EXCEPTIONS
from Style import Style




def catch_debug_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            results = func(*args, **kwargs)
        except Exception as e:
            results = None
            global current_mode
            if current_mode == Mode.DEBUG and isinstance(e, PathException):
                print(e)
                print()
            else:
                raise e
        return results
    return wrapper

class Debug(StrEnum):
    MESSAGE = f"{Fore.LIGHTMAGENTA_EX}(DEBUG)"


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


current_mode = Mode.DEBUG

class Packet():
    class OP(IntEnum):
        SAFE_SEND = 0
        FULL_SEND = 1

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

    def str_dirs_between(self, target: Path):
        num_between = target.parts.index(target.parent.name) - target.parts.index(self.course_name)
        if num_between == 0:
            return ""

        return f"/{'.' * num_between}/"

    def format_str(self, str_or_dst: Path) -> str:
        if self.From == Folders.UNIVERSITY:
            return f"{self.course_name}{self.str_dirs_between(str_or_dst)}{str_or_dst.parent.name if str_or_dst.parent.name != self.course_name else ''}/{str_or_dst.name}"
        elif self.src == str_or_dst:
            return f"{str_or_dst.parent.name if str_or_dst.parent.name != self.course_name else ''}/{str_or_dst.name}"
        elif self.dst == str_or_dst:
            return '/'.join(x for x in str_or_dst.parts[str_or_dst.parts.index(self.course_name):])

    def __str__(self):

        src_path = self.format_str(self.src)
        dst_path = self.format_str(self.dst)

        return (
            f"{Style.TAB_ARROW} SRC:  {src_path}\n"
            f"{Style.TAB_ARROW} DST:  {dst_path}\n"
            + (
                f"{Style.TAB_WARNING} WARNING (Folder Does Not Exist): {Style.UNDERLINE}{self.dst.parent.name}\n"
                if not self.dst.parent.exists() else ""
            )
        )

    def __repr__(self):
        return f"(src: {self.src.parent.name}/{self.src.name}, dst: {self.dst.parent.name}/{self.dst.name})"

    @catch_debug_exceptions
    def print_packet_to_send(self):
        src_str = f"{Style.TAB_SUCCESS} SRC:  {self.src}"
        dst_str = f"{Style.TAB_SUCCESS} DST:  {self.dst}\n"
        error = None

        if self.dst.exists():
            dst_str = f"{Style.TAB_WARNING} DST:  {self.dst}"
            error = DestinationPathAlreadyExists(self.dst)

        elif not self.dst.parent.exists():
            dst_str = f"{Style.TAB_WARNING} DST:  {self.dst}"
            error = DestinationParentDoesNotExist(self.dst)

        elif not self.src.exists():
            src_str = f"{Style.TAB_WARNING} SRC:  {self.src}"
            error = SourcePathDoesNotExist(self.src)

        print(src_str)
        print(dst_str)

        if error:
            raise error

    def send(self, mode: Mode):
        """
        Try to send a packet from self.src to self.dst. Raises errors as defined by PathExceptions.
        """

        try:
            self.print_packet_to_send()
        except PathException as e:
            raise e

        # If reached here no exceptions were raised
        if mode == Mode.SEND:
            self.src.rename(self.dst)


@catch_debug_exceptions
def main():
    colorama_init(autoreset=True)

    file = Path(__file__).stem
    settings = Settings("JSON/settings.json", file)

    with open(settings.json_file, 'r') as json_file:
        course_data: dict = json.load(json_file)

    class_paths = create_class_paths(course_data, settings.basepath)

    folders_to_be_made: set[Path] = set()

    packets_to_be_sent = traverse_folder_packet(settings.src_path, class_paths, course_data, folders_to_be_made)

    folders_to_delete: set[Path] = get_folders_to_delete(packets_to_be_sent)

    try:
        if not packets_to_be_sent:
            print("No files found...")
            return

        mode = user_select_operation_mode()
        global current_mode
        current_mode = mode

        print(f"{Fore.LIGHTMAGENTA_EX if mode == Mode.DEBUG else Fore.GREEN}{mode.upper()} MODE")
        print_packets(packets_to_be_sent, mode)

        if user_continues():
            op = determine_op(folders_to_be_made)
            send_packets(packets_to_be_sent, op, mode)

            print_folders_to_delete(folders_to_delete)
            if user_choose_delete_folders():
                try:
                    delete_folders(folders_to_delete, mode)
                except FolderNotEmpty as e:
                    print(e)

    except KeyboardInterrupt:
        print(f"\nProgram Exited")
        return

    print(Style.RESET)


def print_folders_to_delete(folders_to_delete: set[Path]):
    print(f"{Fore.CYAN}Folders to Delete:")
    for folder in folders_to_delete:
        print(f"{Style.INDENT}{Fore.YELLOW}{Style.ARROW} {Style.UNDERLINE}{folder}{Style.RESET}")

    print()


def delete_folders(folders_to_delete: set[Path], mode: Mode):
    print(f"\n{Fore.CYAN}Folders Deleted:")
    for folder in folders_to_delete:
        if folder.is_dir() and not any(folder.iterdir()):
            if mode == Mode.SEND:
                folder.rmdir()
            print(f"{Style.TAB_SUCCESS} Folder {Style.UNDERLINE}{folder}{Style.RESET}{Fore.GREEN} Deleted")

        else:
            raise FolderNotEmpty(folder)


def user_continues() -> bool:
    return user_choice_bool(f"{Fore.CYAN}Send these files? (y/n):{Fore.YELLOW} ")


def user_choose_delete_folders() -> bool:
    return user_choice_bool(f"{Fore.CYAN}Delete leftover folders? (y/n):{Fore.YELLOW} ")


def get_folders_to_delete(packets_to_be_sent: list[Packet]):
    folders_to_delete = set()

    for packet in packets_to_be_sent:
        if packet.src.is_dir():
            folders_to_delete.add(packet.src)

    return folders_to_delete


def determine_op(folders_to_be_made: set) -> Packet.OP:
    if folders_to_be_made:
        return Packet.OP.FULL_SEND if user_wants_folder_creation() else Packet.OP.SAFE_SEND
    return Packet.OP.FULL_SEND


def user_wants_folder_creation() -> bool:
    """
    Prompts the user if they want to create folders that don't exist (if any)
    in order to send the files.
    """

    while True:
        choice = input(f"{Fore.CYAN}Create Missing Folders? (y/n):{Fore.YELLOW} ").strip().lower()

        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("Invalid Input")


def user_select_operation_mode(delete_lines: bool = True) -> Mode:
    """
    Prompts the user to pick what operation mode to use.
    Returns selected Mode.
    """

    return user_choice_numbered(
        [mode for mode in Mode],
        f"{Fore.CYAN}Select Option:{Fore.YELLOW} ", f"{Fore.CYAN}Operation Modes:",
        delete_lines=delete_lines)


def validate_path(path: Path) -> None:
    """Raise an error if the given path doesn't exist."""
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")


def create_class_paths(university: dict, basepath: Path) -> dict[str, Path]:
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


def print_packets(
        packet_list: list[Packet],
        mode: Mode, recursive_call=False, last_course_code="", last_folder_type=""):

    if not recursive_call:
        mode_str = Debug.MESSAGE if mode == Mode.DEBUG else ""
        print(f"\n{Fore.CYAN}Files to be sent: {mode_str}")

    for packet in packet_list:
        if packet.src.is_dir() and recursive_call == False:
            sub_packet_list = [
                Packet(
                    file, packet.dst.parent / file.name, packet.course_code, packet.course_name, packet.folder_type,
                    packet.file_number) for file in packet.src.iterdir()]

            last_course_code, last_folder_type = print_packets(
                sub_packet_list, mode, True, last_course_code, last_folder_type)
            continue

        if packet.course_code != last_course_code:
            last_course_code = packet.course_code
            print_wait(Delay.SHORT, f"{Fore.CYAN}{packet.course_code}: {packet.course_name}")

        if packet.folder_type != last_folder_type:
            last_folder_type = packet.folder_type
            print_wait(Delay.SHORT, f"{Fore.LIGHTBLUE_EX}  {packet.folder_type}")

        print_wait(Delay.SHORT, packet)

    return last_course_code, last_folder_type


def send_packets(packet_list: list[Packet], op: Packet.OP, mode=Mode.DEBUG, recursive_call=False):

    if not isinstance(op, Packet.OP):
        raise TypeError(f"process_packets: {op} is not a valid OP")

    if not recursive_call:
        mode_str = Debug.MESSAGE if mode == Mode.DEBUG else ""
        print(f"\n{Fore.CYAN}Sending: {mode_str}")

    for packet in packet_list:

        if packet.src.is_dir() and recursive_call == False:
            sub_packet_list = [
                Packet(file, packet.dst.parent / file.name, packet.course_code, packet.course_name, packet.folder_type,
                       packet.file_number) for file in packet.src.iterdir()
            ]

            send_packets(sub_packet_list, op, mode, True)
            continue

        if op == Packet.OP.FULL_SEND and not packet.dst.parent.exists():
            folder_str = f'{Style.UNDERLINE}\"{packet.dst.parent.parent.parent.name}\\{packet.dst.parent.parent.name}\"'
            if mode == Mode.SEND:
                packet.dst.parent.mkdir()
                print(f'{Style.INDENT}{Fore.YELLOW}{Style.ARROW} \"{underline(packet.dst.parent.name)}\"{Fore.YELLOW} Folder Created in {folder_str}')
            else:
                print(f'{Style.INDENT}{Fore.YELLOW}{Style.ARROW} \"{underline(packet.dst.parent.name)}\"{Fore.YELLOW} Folder Will Be Created in {folder_str}')

        try:
            packet.send(mode)
        except SourcePathDoesNotExist as src_e:
            print(src_e)
        except DestinationPathAlreadyExists as dst_e:
            print(dst_e)


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
            split_stem = file.stem.lower().replace("_", " ").replace("-", " ").split()

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
