import json
from pathlib import Path
from move import send_file, user_continues
from Settings import Settings
from Symbols import Symbol
from colorama import Fore

def main():
    file = Path(__file__).stem

    settings_file = "JSON/settings.json"
   
    with open(settings_file, 'r') as settings_json:
        settings: dict = json.load(settings_json)

    if Path.cwd().anchor == '/':
        dst_folder = Path(settings[file][Settings.WSL_DST_PATH])
        src_folder = Path(settings[file][Settings.WSL_SRC_PATH])
    else:
        dst_folder = Path(settings[file][Settings.WIN_DST_PATH])
        src_folder = Path(settings[file][Settings.WIN_SRC_PATH])

    files_to_be_sent = []

    for file in src_folder.iterdir():
        if file.suffix in settings[file][Settings.PATHS_TO_CHECK]:
            files_to_be_sent.append(
                {
                    "src": src_folder / file.name,
                    "dst": dst_folder / file.name
                }
            )

    if len(files_to_be_sent) == 0:
        print("No files were found")
    else:
        for file in files_to_be_sent:
            print(f'{Symbol.STRAIGHT_ARROW}  From:   {file["src"]}')
            print(f'{Symbol.STRAIGHT_ARROW}    To:   {file["dst"]}\n')

        if user_continues():
            for file in files_to_be_sent:
                send_file(file["src"], file["dst"])


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
