import json

from move import user_continues, pretty_print_substring, return_pretty_print_string
from colorama import Fore
from pathlib import Path
from Settings import Settings
from Symbols import Symbol


def main():
    file = Path(__file__).stem
    
    settings = set_up_settings("JSON/settings.json", file)

    with open(settings[Settings.JSON_FILE], 'r') as extension_file:
        extensions = json.load(extension_file)

    if Path.cwd().anchor == '/':
        srcFolder = Path(settings[Settings.WSL_SRC_PATH])
    else:
        srcFolder = Path(settings[Settings.WIN_SRC_PATH])

    files_to_be_sent = get_files_to_be_sent(extensions, srcFolder)

    if len(files_to_be_sent) == 0:
        print("No files were found")
    else:
        for file in files_to_be_sent:
            print_file(file, extensions)

        if user_continues():
            for file in files_to_be_sent:
                send_file(file["src"], file["dst"], send_enabled=True)


def set_up_settings(settings_file, current_file):
    if not Path(settings_file).exists():
        raise FileNotFoundError(settings_file)
    with open(settings_file, 'r') as settings_json:
        settings: dict = json.load(settings_json)
    return settings[current_file]


def get_files_to_be_sent(extensions, srcFolder):
    files_to_be_sent = []
    for file in srcFolder.iterdir():
        for folder in extensions:
            if file.suffix in extensions[folder] and file.name not in extensions:
                files_to_be_sent.append(
                    {
                        "src":  srcFolder / file,
                        "dst": srcFolder / Path(f"{(extensions[folder][file.suffix])}/{file.name}")
                    }
                )

    return files_to_be_sent


def print_file(file: dict[str, Path], extensions: dict[str, str]):
    src_string = return_pretty_print_string(str(file["src"]), str(file["src"].name), start="", color=Fore.CYAN)
    pretty_print_substring(src_string, file["src"].suffix, start=f"{Symbol.ARROW}  From:  ", color=Fore.YELLOW)

    dst_string = return_pretty_print_string(str(file["dst"]), str(file["dst"].name), start="", color=Fore.CYAN)

    ext_path = extensions[file['dst'].parent.parent.name][file["src"].suffix].split("\\")[-1]
    dst_string = return_pretty_print_string(dst_string, file["src"].suffix, start="", color=Fore.YELLOW)

    pretty_print_substring(dst_string, ext_path, start=f"{Symbol.ARROW}    To:  ", end='\n', color=Fore.YELLOW)


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
