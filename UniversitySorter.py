from pathlib import Path
from move import user_continues
from colorama import Fore
import json
from Symbols import Symbol
from Settings import Settings


def main():
    file = Path(__file__).stem
    settings_file = "JSON/settings.json"
    if not Path(settings_file).exists():
        raise FileNotFoundError(settings_file)

    with open(settings_file, 'r') as settings_json:
        settings: dict = json.load(settings_json)

    # If I am accessing these scripts from my WSL instance, will have different path structure
    if Path.cwd().anchor == '/':
        basepath = Path(settings[file][Settings.WSL_BASEPATH])
        src_folder_path = Path(settings[file][Settings.WSL_SRC_PATH])

    else:
        basepath = Path(settings[file][Settings.WIN_BASEPATH])
        src_folder_path = Path(settings[file][Settings.WIN_SRC_PATH])

    if not basepath.exists():
        raise FileNotFoundError(basepath)
    if not src_folder_path.exists():
        raise FileNotFoundError(src_folder_path)

    with open(settings[file][Settings.JSON_FILE], 'r') as json_file:
        university: dict = json.load(json_file)

    classes = {}
    for year, semesters in university.items():
        for semester, class_list in semesters.items():
            folder_path: Path = basepath / year / semester
            class_paths: Path = get_class_paths(folder_path)
            classes.update(dict(zip(class_list, class_paths)))

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
        file_name_1 = file.name[:9].replace(" ", "").replace("-", "").replace("_", "").upper().strip()

        if file_name_1 in class_folders:
            files_to_be_sent.append({
                                    "src": file,
                                    "dst": class_folders[file_name_1] / file.name,
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
            print(Fore.GREEN + f'{Symbol.SUCCESS} From:  {src}')
            print(Fore.RED + f'{Symbol.FAILURE}   To:  {dst}')
            print(Fore.YELLOW + f"WARNING: File Already Exists")
        else:
            if send_enabled:
                src.rename(dst)
            print(Fore.GREEN + f'{Symbol.SUCCESS} From:  {src}')
            print(Fore.GREEN + f'{Symbol.SUCCESS}   To:  {dst}', end="")

    except FileNotFoundError as e:
        print(Fore.YELLOW + f'{Symbol.FAILURE} From:  {src}')
        print(Fore.YELLOW + f'{Symbol.FAILURE}   To:  {dst}')
        print(Fore.RED + f"ERROR: File Not Found {e}")

    except Exception as error:
        print(error)

    print(Fore.RESET + "\n")


if __name__ == "__main__":
    main()
