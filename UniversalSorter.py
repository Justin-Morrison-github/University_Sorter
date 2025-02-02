from pathlib import Path
from move import user_continues
from colorama import Fore
import json
from ANSI import ANSI
from Settings import Settings


def main():
    file = Path(__file__).stem
    settings_file = "JSON/settings.json"
    if not Path(settings_file).exists():
        raise FileNotFoundError(settings_file)

    with open(settings_file, 'r') as settings_json:
        settings: dict = json.load(settings_json)

    basepath = Path(settings[file][Settings.WIN_BASEPATH])
    if not basepath.exists():
        raise FileNotFoundError(basepath)

    src_folder_path = Path(settings[file][Settings.WIN_SRC_PATH])
    if not src_folder_path.exists():
        raise FileNotFoundError(src_folder_path)

    json_path = settings[file][Settings.JSON_FILE]
    with open(json_path, 'r') as json_file:
        flags: dict = json.load(json_file)

    files_to_be_sent = traverse_folder(src_folder_path, flags)
    print(files_to_be_sent)
    if len(files_to_be_sent) == 0:
        print("No files were found")
    else:
        for file in files_to_be_sent:
            print(f'{ANSI.ARROW}  From:   {file["src"]}')
            print(f'{ANSI.ARROW}    To:   {file["dst"]}\n')

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


def traverse_folder(src_folder_path: Path, flags: dict) -> list[dict]:
    files_to_be_sent = []

    for file in src_folder_path.iterdir():
        # Check if the file stem contains any of the specified words in flags["Filenames"]
        for word, destinations in flags["Filenames"].items():
            if word in file.stem:
                if word == "Cardwise":
                    year = file.stem.split()[-1]
                    if year in destinations:  # Ensure the year is valid in the destination mapping
                        files_to_be_sent.append({
                            "src": file,
                            "dst": Path(destinations[year]) / file.name,
                        })
                        break  # Found a match, exit the loop early

        else:  # Only executes if the 'Filenames' loop did not break
            # Check if the file's extension matches any in flags["Extensions"]
            if file.suffix in flags["Extensions"]:
                files_to_be_sent.append({
                    "src": file,
                    "dst": Path(flags["Extensions"][file.suffix]) / file.name,
                })

            # elif file.is_dir():
            #     files_to_be_sent += traverse_folder(file, flags)

    return files_to_be_sent


def send_file(src: Path, dst: Path, send_enabled=False) -> None:
    """
    Sends a file from src to dst. Prints out certain results
    """

    try:
        if dst.exists():
            print(Fore.GREEN + f'{ANSI.SUCCESS} From:  {src}')
            print(Fore.RED + f'{ANSI.FAILURE}   To:  {dst}')
            print(Fore.YELLOW + f"WARNING: File Already Exists")
        else:
            if send_enabled:
                src.rename(dst)
            print(Fore.GREEN + f'{ANSI.SUCCESS} From:  {src}')
            print(Fore.GREEN + f'{ANSI.SUCCESS}   To:  {dst}', end="")

    except FileNotFoundError as e:
        print(Fore.YELLOW + f'{ANSI.FAILURE} From:  {src}')
        print(Fore.YELLOW + f'{ANSI.FAILURE}   To:  {dst}')
        print(Fore.RED + f"ERROR: File Not Found {e}")

    except Exception as error:
        print(error)

    print(Fore.RESET + "\n")


if __name__ == "__main__":
    main()
