import json

from move import user_continues
from colorama import Fore
from pathlib import Path
from Settings import Settings
from ANSI import ANSI
from PrettyPrint import highlight_substr

def main():
    file = Path(__file__).stem
    
    settings = Settings("JSON/settings.json", file)
    root = settings.src_path

    with open(settings.json_file, 'r') as extension_file:
        extensions = json.load(extension_file)

    files_to_be_sent = get_files_to_be_sent(extensions, root)

    if len(files_to_be_sent) == 0:
        print("No files were found")
    else:
        for file in files_to_be_sent:
            print_file(file, extensions)

        if user_continues():
            for file in files_to_be_sent:
                send_file(file["src"], file["dst"], send_enabled=False)


def get_files_to_be_sent(extensions, srcFolder):
    files_to_be_sent = []
    for file in srcFolder.iterdir():
        for folder in extensions:
            if file.suffix in extensions[folder] and file.name not in extensions:
                files_to_be_sent.append(
                    {
                        "src": srcFolder / file,
                        "dst": srcFolder / Path(f"{(extensions[folder][file.suffix])}/{file.name}")
                    }
                )

    return files_to_be_sent


def get_pretty_src_string(file: dict[str, Path]):
    highlight_name = highlight_substr(str(file["src"]), str(file["src"].name), color=Fore.CYAN)
    highlight_path= highlight_substr(highlight_name, file["src"].suffix, color=Fore.YELLOW)

    return f"{ANSI.ARROW} From: {highlight_path}"


def get_pretty_dst_string(file: dict[str, Path], extensions: dict[str, str]):
    highlight_name = highlight_substr(str(file["dst"]), str(file["dst"].name), color=Fore.CYAN)
    highlight_path = highlight_substr(highlight_name, file["dst"].parent.name, color=Fore.YELLOW)

    return f"{ANSI.ARROW}   To: {highlight_path}"

def print_file(file: dict[str, Path], extensions: dict[str, str]):
    src_string = get_pretty_src_string(file)
    print(src_string)

    dst_string = get_pretty_dst_string(file, extensions)
    print(dst_string + "\n")

class FileSuccess():
    def __init__(self, src:Path, dst:Path):
        message = (
            f"{Fore.GREEN}{ANSI.B_SUCCESS} {src.name}\n"
            f"{ANSI.INDENT}{ANSI.B_SUCCESS} From:  {src}\n"
            f"{ANSI.INDENT}{ANSI.B_SUCCESS}   To:  {dst}{Fore.RESET}"
        )

        print(message)


def format_error_message(src:Path, dst:Path, e):
    if isinstance(e, FileExistsError):
        return (
            f"{Fore.YELLOW}{ANSI.WARNING} {src.name}  (WARNING: File Already Exists)\n"
            f"{ANSI.INDENT}{Fore.GREEN}{ANSI.B_SUCCESS} From:  {src}\n"
            f"{ANSI.INDENT}{Fore.YELLOW}{ANSI.WARNING}   To:  {dst}{Fore.RESET}\n"
        )
    
    elif isinstance(e, FileNotFoundError):
        return (
            f"{Fore.RED}{ANSI.FAILURE}{src.name}  (ERROR: File Not Found)\n"
            f"{ANSI.INDENT}{Fore.RED}{ANSI.FAILURE} From: {src}\n"
            f"{ANSI.INDENT}{Fore.GREEN}{ANSI.SUCCESS}   To:  {dst}{Fore.RESET}"
        )

def send_file(src: Path, dst: Path, send_enabled=False) -> None:
    """
    Sends a file from src to dst. Prints out certain results
    """

    try:
        if dst.exists():
            raise FileExistsError(format_error_message(src, dst, FileExistsError()))
        elif not src.exists():
            raise FileNotFoundError(format_error_message(src, dst, FileNotFoundError()))
        
        if send_enabled:
            src.rename(dst)
        FileSuccess(src, dst)
        
    except Exception as error:
        print(error)

    print("\n")


if __name__ == "__main__":
    main()
