from pathlib import Path
from enum import StrEnum
from move import user_continues
from colorama import Fore
import json
from ANSI import ANSI
from Settings import Settings


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

    def __repr__(self):
        return self.value


class Packet():
    def __init__(self, src: Path, dst: Path, parent: Path, course: Folders, course_name: str, file_number: int = None):
        self.src = src
        self.dst = dst
        self.parent = parent
        self.course = course
        self.name = self.src.stem
        self.course_name = course_name

        if file_number:
            self.file_number = file_number
        else:
            self.file_number = None

        self.update_packet_if_needed()

    def __str__(self):
        return f"     {ANSI.ARROW} SRC:  {self.src.parent.name}\\{self.src.name}\n     {ANSI.ARROW} DST:  {self.dst.parent.name}\\{self.dst.name}\n"

    def __repr__(self):
        return f"(src: {self.src.parent.name}\\{self.src.name}, dst: {self.dst.parent.name}\\{self.dst.name})"

    def update_packet_if_needed(self):
        split_stem = self.src.stem.lower().split()
        dst_folder = ""

        if self.parent == Folders.ASSIGNMENT or self.parent == Folders.LAB:
            index = split_stem.index(self.parent.lower())  # Index of the folder
            self.file_number = int(split_stem[index + 1])  # The file number comes after the folder, Ex.) Assignment 5
            dst_folder = f'{self.parent} {self.file_number}'

        new_dst: Path = self.dst.parent / dst_folder / self.src.name
        self.dst = new_dst


def main():
    file = Path(__file__).stem

    settings = Settings("JSON/settings.json", file)

    with open(settings.json_file, 'r') as json_file:
        course_data: dict = json.load(json_file)

    # setup_folders(root, course_dict)
    packets_to_be_sent = make_packets(settings.basepath, course_data)
    if len(packets_to_be_sent) == 0:
        print("No files found...")
    else:
        process_packets(packets_to_be_sent, "print")

        if user_continues():
            process_packets(packets_to_be_sent, "send", True)


# def setup_folders(root: Path, courses: dict):
#     for course in root.iterdir():
#         if course.name in courses:
#             class_path = root / course
#             for folder in courses[course.name]:
#                 dir = Path(class_path / folder)
#                 if not dir.exists():
#                     print(f"Making {dir.name}")
#                     dir.mkdir()


def make_packets(root: Path, course_dict: dict):
    packet_list = []
    for year, semesters in course_dict.items():
        for semester, courses in semesters.items():
            for course, data in courses.items():
                class_path: Path = root / year / semester / data['name']
                if not class_path.exists():
                    raise FileNotFoundError(class_path)

                for folder in data['folders']:
                    matching_files = list(class_path.glob(f"* {folder} *"))
                    if matching_files:
                        dest_folder: Path = class_path / Folders[folder]
                        for file in matching_files:
                            dest = dest_folder / file.name
                            packet = Packet(file, dest, Folders[folder], course,
                                            course_dict[year][semester][course]['name'])
                            packet_list.append(packet)

    return packet_list


def process_packets(packet_list: list[Packet], command="print", send_enabled=False):
    action = "Sending" if send_enabled else "Files to be sent"
    print(f"\n{action}:")
    last_course = ""
    last_folder = ""

    for packet in packet_list:
        if packet.course != last_course:
            print(f"{Fore.CYAN}{packet.course}: {packet.course_name}{Fore.RESET}")
            last_course = packet.course

        if packet.parent != last_folder:
            print(f"{Fore.YELLOW}  {packet.parent}{Fore.RESET}")
            last_folder = packet.parent

        if command == "print":
            print(packet)
        elif command == "send":
            if send_enabled:
                send_packet(packet, send_enabled)
            else:
                print("Send is Not Enabled")


def send_packet(packet: Packet, send_enabled=False) -> None:
    """
    Sends a packet from packet.src to packet.dst. Prints out success or failure
    """

    try:
        if packet.dst.exists():
            print(f"\t{Fore.GREEN}{ANSI.SUCCESS} From:  {packet.src}")
            print(f"\t{Fore.RED}{ANSI.FAILURE}   To:  {packet.dst}")
            print(f"\t{Fore.YELLOW}WARNING: File Exists{ANSI.STRAIGHT_ARROW}  {packet.dst}")
        else:
            if send_enabled:
                packet.src.rename(packet.dst)
            print(f"\t{Fore.GREEN}{ANSI.SUCCESS} From:  {packet.src}")
            print(f"\t{Fore.GREEN}{ANSI.SUCCESS}   To:  {packet.dst}", end="")

    except FileNotFoundError as e:
        print(f"\t{Fore.YELLOW}{ANSI.FAILURE} From:  {packet.src}")
        print(f"\t{Fore.YELLOW}{ANSI.FAILURE}   To:  {packet.dst}")
        print(f"\t{Fore.RED}{e}")

    print(Fore.RESET + "\n")


if __name__ == "__main__":
    main()
