from pathlib import Path
from move import user_continues
from colorama import Fore


def main():
    basepath = Path("C:\\Users\\morri\\OneDrive\\University")
    if not basepath.exists():
        print(f"Error {basepath} does not exist")
        return

    university = {
        "01_First-Year Classes": {
            "FALL": ["MATH 1004", "CHEM 1101", "ECOR 1048", "ECOR 1055", "ECOR 1057", "ECOR 1046", "ECOR 1045", "PHYS 1003", "ECOR 1047"],
            "WINTER": ["ECOR 1043", "ECOR 1042", "PHYS 1004", "ECOR 1056", "GEOG 1020", "MATH 1104", "ECOR 1044", "ECOR 1041"],
        },
        "02_Second-Year Classes": {
            "FALL": ["ELEC 2501", "COOP 1000", "MATH 1005", "SYSC 2310", "COMP 1805", "SYSC 2006"],
            "WINTER": ["SYSC 2100", "CCDP 2100", "SYSC 2320", "COMP 2804", "SYSC 2004"],
        }
    }

    classes = {}
    for year, semesters in university.items():
        for semester, class_list in semesters.items():
            folder_path: Path = basepath / year / semester
            class_paths: Path = get_class_paths(folder_path)
            classes.update(dict(zip(class_list, class_paths)))

    src_folder_path: Path = Path("C:\\Users\\morri\\Downloads")
    files_to_be_sent = traverse_folder(src_folder_path, classes)

    if len(files_to_be_sent) == 0:
        print("No files were found")
    else:
        for file in files_to_be_sent:
            print(f'\u2794  From:   {file["src"]}')
            print(f'\u2794    To:   {file["dst"]}\n')

        if user_continues():
            send_files(files_to_be_sent, send_enabled=True)


def send_files(files_to_be_sent: list, send_enabled=False):
    for file in files_to_be_sent:
        send_file(file["src"], file["dst"], send_enabled=send_enabled)


def get_class_paths(folder_path: Path):
    classes = []
    for folder in folder_path.iterdir():
        path: Path = folder_path / folder
        if path.is_dir():
            classes.append(path)

    return classes


def traverse_folder(src_folder_path: Path, class_folders: dict) -> list[dict]:
    files_to_be_sent = []

    for file in src_folder_path.iterdir():
        file_name_1 = file.name[:9].replace("-", " ").replace("_", " ").upper().strip()
        file_name_2 = file.name[:4] + " " + file.name[4:8]

        if file_name_1 in class_folders:
            files_to_be_sent.append({
                                    "src": file,
                                    "dst": class_folders[file_name_1] / file.name,
                                    })
        elif file_name_2 in class_folders:
            files_to_be_sent.append({
                                    "src": file,
                                    "dst": class_folders[file_name_2] / file.name,
                                    })
        elif file.is_dir():
            files_to_be_sent += traverse_folder(file, class_folders)

    return files_to_be_sent


def send_file(src: Path, dst: Path, send_enabled=False) -> None:
    """
    Sends a file from src to dst. Prints out certain results
    """

    try:
        if dst.exists():
            print(Fore.GREEN + f'\u2705 From:  {src}')
            print(Fore.RED + f'\u274C   To:  {dst}')
            print(Fore.YELLOW + f"WARNING: File Already Exists")
        else:
            if send_enabled:
                src.rename(dst)
            print(Fore.GREEN + f'\u2705 From:  {src}')
            print(Fore.GREEN + f'\u2705   To:  {dst}', end="")

    except FileNotFoundError as e:
        print(Fore.YELLOW + f'\u274C From:  {src}')
        print(Fore.YELLOW + f'\u274C   To:  {dst}')
        print(Fore.RED + f"ERROR: File Not Found {e}")

    except Exception as error:
        print(error)

    print(Fore.RESET + "\n")


if __name__ == "__main__":
    main()
