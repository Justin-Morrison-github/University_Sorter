import os, sys

curr_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_dir)

from pathlib import Path
from enum import IntEnum, StrEnum, auto
from colorama import Fore, init as colorama_init
import json
from Settings import Settings
from typing import Optional
from terminal_utils import user_choice_bool, user_choice_numbered, Delay, print_wait
from string_utils import underline, path_from_substring
from exceptions import DestinationParentDoesNotExist, PathException, SourcePathDoesNotExist, DestinationPathAlreadyExists, FolderNotEmpty
from Style import Style
import copy


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
    SEND_MKDIR = auto()


current_mode = Mode.DEBUG


class Folder(StrEnum):
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


class Status(StrEnum):
    RETRIEVED = auto()
    SENDING = auto()


class Packet():
    def __init__(self, src: Path, dst: Path, course_code: str, course_name: str, folder_type: Folder,
                 file_number: int = None, status: Status = Status.RETRIEVED):
        self.src: Path = src
        self.dst: Path = dst
        self.course_code: str = course_code
        self.file_name: str = self.src.stem
        self.course_name: str = course_name
        self.file_number: int = file_number
        self.folder_type: Folder = folder_type
        self.status = status
        self.error = None

    # TODO: Make better
    def __str__(self):
        if self.status == Status.RETRIEVED:

            src_path = path_from_substring(self.src, Folder.DOWNLOADS)
            dst_path = path_from_substring(self.dst, self.course_name)

            return (
                f"{Style.TAB_ARROW} SRC:  {src_path}\n"
                f"{Style.TAB_ARROW} DST:  {dst_path}\n"
                + (
                    f"{Style.TAB_WARNING} WARNING (Folder Does Not Exist): {Style.UNDERLINE}{self.dst.parent.name}\n"
                    if not self.dst.parent.exists() else ""
                )
            )
        elif self.status == Status.SENDING:
            src_str = path_from_substring(self.src, Folder.DOWNLOADS)
            dst_str = path_from_substring(self.dst, self.course_name)

            src_start = Style.TAB_SUCCESS
            dst_start = Style.TAB_SUCCESS

            if self.dst.exists() or not self.dst.parent.exists():
                dst_start = Style.TAB_WARNING

            if not self.src.exists():
                src_start = Style.TAB_WARNING

            end_str = '' if not self.error else f"{self.error}"
            return (
                f"{src_start} SRC:  {src_str}\n"
                f"{dst_start} DST:  {dst_str}\n"
                f"{end_str}"
            )

    def print_hierarchy(
            self, src_folder_path: str, depth=0, arrow_color=Fore.WHITE, count_color=Fore.WHITE, file_color=Fore.CYAN,
            size_color=Fore.GREEN):
        depth += 1
        count = 0
        for file in Path(src_folder_path).iterdir():
            path = Path(src_folder_path) / Path(file).name

            print(f"{Style.INDENT * (depth)}", end=" ")

            print(f"{arrow_color}{Style.ARROW}", end=" ")

            count += 1
            print(f"{count_color}{count:03d}", end=" ")

            print(f'{file_color}{file.name}', end="")

            size = 100
            print(f"{size_color} {size}"),

            if path.is_dir():
                self.print_hierarchy(path, depth, arrow_color, count_color, file_color,
                                     size_color)

    def pretty_print(self, parent):
        self.print_hierarchy(parent)

    def __repr__(self):
        return f"(src: {self.src.parent.name}/{self.src.name}, dst: {self.dst.parent.name}/{self.dst.name})"

    # @catch_debug_exceptions
    def check_packet_send(self):

        if self.dst.exists():
            self.error = DestinationPathAlreadyExists(self.dst)

        elif not self.dst.parent.exists():
            self.error = DestinationParentDoesNotExist(self.dst)

        elif not self.src.exists():
            self.error = SourcePathDoesNotExist(self.src)

        # if self.error:
        #     raise self.error

    def send(self, mode: Mode):
        """
        Try to send a packet from self.src to self.dst. Raises errors as defined by PathExceptions.
        """
        self.status = Status.SENDING
        try:
            self.check_packet_send()
            print(self)
            if self.error:
                raise self.error
        except DestinationParentDoesNotExist as e:
            if mode == Mode.SEND_MKDIR:
                pass
            else:
                raise e

        except PathException as e:
            # print(e)
            raise e

        # If reached here no exceptions were raised
        if mode in [Mode.SEND, Mode.SEND_MKDIR]:
            self.src.rename(self.dst)


class SchoolSorter():
    def __init__(self):
        self._start_file: Path = Path(__file__).stem
        self.settings: Settings = Settings("app/json/settings.json", self._start_file)

        with open(self.settings.json_file, 'r') as json_file:
            self.university_data: dict[str, dict[str, dict]] = json.load(json_file)

        self.class_paths: dict[str, Path] = self.create_class_paths()
        self.folders_to_be_made: set[Path] = set()
        self.packets_to_be_sent: list[Packet] = self.get_packets(self.settings.src_path)
        self.folders_to_delete: set[Path] = self.get_folders_to_delete()
        self.mode: Mode = Mode.DEBUG

    def main(self):
        colorama_init(autoreset=True)

        try:
            if not self.packets_to_be_sent:
                print("No files found...")
                return

            self.mode: Mode = self.user_select_operation_mode()

            print(f"{Fore.LIGHTMAGENTA_EX if self.mode == Mode.DEBUG else Fore.GREEN}{self.mode.upper()} MODE")
            self.print_packets()

            if self.user_continues():
                self.send_packets()

                self.print_folders_to_delete()
                if self.user_choose_delete_folders():
                    try:
                        self.delete_folders()
                    except FolderNotEmpty as e:
                        print(e)

        except KeyboardInterrupt:
            print(f"\nProgram Exited")
            return

    def get_folders_to_delete(self) -> set[Path]:
        folders_to_delete: set[Path] = set()

        for packet in self.packets_to_be_sent:
            if packet.src.is_dir():
                folders_to_delete.add(packet.src)

        return folders_to_delete

    def print_folders_to_delete(self) -> None:
        print(f"{Fore.CYAN}Folder to Delete:")
        for folder in self.folders_to_delete:
            print(f"{Style.TAB_WARNING} {Style.UNDERLINE}{folder}{Style.RESET}")

        print()

    def delete_folders(self):
        print(f"\n{Fore.CYAN}Folder Deleted:")
        for folder in self.folders_to_delete:
            if folder.is_dir() and not any(folder.iterdir()):
                if self.mode == Mode.SEND:
                    folder.rmdir()
                print(f"{Style.TAB_SUCCESS} Folder {Style.UNDERLINE}{folder}{Style.RESET}{Fore.GREEN} Deleted")

            else:
                raise FolderNotEmpty(folder)

    def user_continues(self) -> bool:
        return user_choice_bool(f"{Fore.CYAN}Send these files? (y/n):{Fore.YELLOW} ")

    def user_choose_delete_folders(self) -> bool:
        return user_choice_bool(f"{Fore.CYAN}Delete leftover folders? (y/n):{Fore.YELLOW} ")

    def user_select_operation_mode(self, delete_lines: bool = True) -> Mode:
        """
        Prompts the user to pick what operation mode to use.
        Returns selected Mode.
        """

        return user_choice_numbered(
            [mode for mode in Mode],
            f"{Fore.CYAN}Select Option:{Fore.YELLOW} ", f"{Fore.CYAN}Operation Modes:",
            delete_lines=delete_lines)

    def validate_path(self, path: Path) -> None:
        """Raise an error if the given path doesn't exist."""
        if not path.exists():
            raise FileNotFoundError(f"Path not found: {path}")

    def create_class_paths(self) -> dict[str, Path]:
        classes = {}
        for year, semesters in self.university_data.items():
            for semester, class_list in semesters.items():
                folder_path: Path = self.settings.dst_path / year / semester
                class_paths: list[Path] = self.get_class_paths(folder_path)
                classes.update(dict(zip(class_list, class_paths)))

        return classes

    def get_class_paths(self, folder_path: Path) -> list[Path]:
        class_paths = []
        for folder in folder_path.iterdir():
            path: Path = folder_path / folder
            if path.is_dir():
                class_paths.append(path)

        return class_paths

    def get_packets(self, src_folder_path: Path = None) -> list[Packet]:
        if src_folder_path is None:
            src_folder_path = self.settings.src_path

        files_to_be_sent = []

        # Initialize a stack with the source folder path
        stack = [src_folder_path]

        while stack:
            current_folder = stack.pop()

            for file in current_folder.iterdir():
                tag = file.name[:9].replace(" ", "").replace("-", "").replace("_", "").upper().strip()

                if tag in self.class_paths:
                    parent_path: Path = self.class_paths[tag]
                    course_name = parent_path.name

                    dst: Path = parent_path / file.name
                    for folder in [Folder[folder]
                                   for folder in self.university_data[parent_path.parent.parent.name]
                                   [parent_path.parent.name][tag]["folders"]]:

                        if folder in file.stem:
                            dst = self.find_path_within_parent(parent_path, file, folder)
                            break

                    packet = Packet(file, dst, tag, course_name, folder)
                    files_to_be_sent.append(packet)

                elif file.is_dir() and file.parent == src_folder_path:
                    # If it's a directory, add it to the stack for later processing
                    stack.append(file)

        return files_to_be_sent

    def print_packets(self):
        if not isinstance(self.mode, Mode):
            raise TypeError(f"process_packets: {self.mode} is not a valid Mode")

        mode_str = Debug.MESSAGE if self.mode == Mode.DEBUG else ""
        print(f"\n{Fore.CYAN}Files to be sent: {mode_str}")

        last_course_code = ""
        last_folder_type = ""

        # Initialize a stack for the packets to be processed, make deep copy to prevent mutation
        stack = copy.deepcopy(self.packets_to_be_sent)

        while stack:
            packet = stack.pop()

            if packet.src.is_dir() and packet.src.parent == self.settings.src_path:
                # If the packet is a directory, add its contents to the stack
                sub_packet_list = [
                    Packet(
                        file, packet.dst.parent / file.name, packet.course_code, packet.course_name, packet.folder_type,
                        packet.file_number) for file in packet.src.iterdir()
                ]
                stack.extend(sub_packet_list)  # Add the sub-packets to the stack
                continue

            if packet.course_code != last_course_code:
                last_course_code = packet.course_code
                print_wait(Delay.SHORT, f"{Fore.CYAN}{packet.course_code}: {packet.course_name}")

            if packet.folder_type != last_folder_type:
                last_folder_type = packet.folder_type
                print_wait(Delay.SHORT, f"{Fore.LIGHTBLUE_EX}  {packet.folder_type}")

            print_wait(Delay.SHORT, packet)

    def send_packets(self):
        if not isinstance(self.mode, Mode):
            raise TypeError(f"send_packets: {self.mode} is not a valid Mode")

        mode_str = Debug.MESSAGE if self.mode == Mode.DEBUG else ""
        print(f"\n{Fore.CYAN}Sending: {mode_str}")

        # Initialize a stack for the packets to be processed
        stack = copy.deepcopy(self.packets_to_be_sent)

        while stack:
            packet = stack.pop()

            if packet.src.is_dir():
                # If the packet is a directory, add its contents to the stack
                sub_packet_list = [
                    Packet(
                        file, packet.dst.parent / file.name, packet.course_code, packet.course_name, packet.folder_type,
                        packet.file_number) for file in packet.src.iterdir()
                ]
                stack.extend(sub_packet_list)  # Add the sub-packets to the stack
                continue

            folder_str = f'{Style.UNDERLINE}\"{packet.dst.parent.parent.parent.name}\\{packet.dst.parent.parent.name}\"'
            if self.mode == Mode.SEND_MKDIR and not packet.dst.parent.exists():

                if self.mode == Mode.SEND_MKDIR:
                    packet.dst.parent.mkdir()
                    print(f'{Style.TAB_WARNING} \"{underline(packet.dst.parent.name)}\"{Fore.YELLOW} Folder Created in {folder_str}')
            try:
                packet.send(self.mode)
                # if packet.src.parent != self.settings.src_path:
                #     packet.pretty_print(packet.src.parent)
            except DestinationParentDoesNotExist as e:
                if self.mode == Mode.SEND:
                    print(
                        f'{Style.TAB_WARNING} Enable SEND_MKDIR Mode to create missing folder \"{underline(packet.dst.parent.name)}\"{Fore.YELLOW} in {folder_str}\n')
                elif self.mode == Mode.DEBUG:
                    print()

            except PathException as e:
                pass

    # TODO Remove Class Code from folder when being added (Lab/SYSC 2320 Lab 5 ---> Lab/Lab 5)

    def find_or_create_folder(self, parent: Path, folder_name: str) -> Optional[str]:
        """Search for a folder matching the target name in the parent directory."""

        if not parent.exists():
            parent = self.find_or_create_folder(parent.parent, folder_name.split()[0])

        for folder in parent.glob(f"*{folder_name}*"):
            if folder.is_dir():
                return folder

        new_folder = parent / folder_name
        if not new_folder.exists():
            self.folders_to_be_made.add(new_folder)

        return new_folder

    def find_path_within_parent(self, parent: Path, file: Path, folder: Folder):

        # If there is a number associated with folder (e.g., "Assignment 5")
        if folder in [Folder.ASSIGNMENT, Folder.LAB, Folder.LECTURE, Folder.TUTORIAL]:

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
            matching_folder_path = self.find_or_create_folder(parent / folder, target_folder)

        elif folder in [Folder.INFO, Folder.REVIEW, Folder.PASS, Folder.TEXTBOOK, Folder.WOOCLAP]:
            matching_folder_path = self.find_or_create_folder(file.parent, folder)
        else:
            return parent / file

        return matching_folder_path / file.name


if __name__ == "__main__":
    colorama_init(autoreset=True)
    app = SchoolSorter()
    app.main()
    print(Style.RESET)
