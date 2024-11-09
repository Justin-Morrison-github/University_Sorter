import json

from move import send_file, user_continues, pretty_print_substring, return_pretty_print_string
from colorama import Fore
from pathlib import Path
from Settings import Settings


def main():
    settings_file = "JSON/settings.json"
    if not Path(settings_file).exists():
        raise FileNotFoundError(settings_file)
    with open(settings_file, 'r') as settings_json:
        settings: dict = json.load(settings_json)

    extensions = {
        # AUDIO
        '.mp3': 'AUDIO\\MP3',
        '.wav': 'AUDIO\\WAV',

        # CODE
        '.py':   'CODE\\PYTHON',
        '.cs':   'CODE\\C#',
        '.c':    'CODE\\C',
        '.java': 'CODE\\JAVA',

        # FOLDERS
        '.zip': 'FOLDERS\\ZIP',
        '':     'FOLDERS\\Folders',

        # IMAGES
        '.pdf':  'IMAGES\\PDF',
        '.png':  'IMAGES\\PNG',
        '.jpg':  'IMAGES\\JPG',
        '.ico':  'IMAGES\\ICON',
        '.HEIC': 'IMAGES\\HEIC',

        # INSTALLERS
        '.exe': 'INSTALLERS\\EXE',
        '.msi': 'INSTALLERS\\MSI',

        # OTHER
        '.f3d':           'OTHER\\FUSION',
        '.otf':           'OTHER\\FONTS',
        '.metadata':      'OTHER\\METADATA',
        '.tracktionedit': 'OTHER\\TRACKTION',
        '.vsix':          'OTHER\\VSIX',

        # TEXT
        '.txt':  'TEXT\\TXT',
        '.docx': 'TEXT\\WORD',
        '.xlsx': 'TEXT\\EXCEL',
        '.ppt':  'TEXT\\POWERPOINT',
        '.pptx': 'TEXT\\POWERPOINT'
    }

    if Path.cwd().anchor == '/':
        srcFolder = Path(settings[file][Settings.WSL_SRC_PATH])
    else:
        srcFolder = Path(settings[file][Settings.WIN_SRC_PATH])
    files_to_be_sent = []

    for file in srcFolder.iterdir():
        if file.suffix in extensions:
            files_to_be_sent.append(
                {
                    "src":  srcFolder / file,
                    "dst": srcFolder / Path(f"{(extensions[file.suffix])}/{file.name}"),
                }
            )

    if len(files_to_be_sent) == 0:
        print("No files were found")
    else:
        for file in files_to_be_sent:
            print_file(file, extensions)

        if user_continues():
            for file in files_to_be_sent:
                send_file(file["src"], file["dst"], send_enabled=True)


def print_file(file: dict[str, Path], extensions: dict[str, str]):
    src_string = return_pretty_print_string(str(file["src"]), str(file["src"].name), start="", color=Fore.CYAN)
    pretty_print_substring(src_string, file["src"].suffix, start="\u2794  From:  ", color=Fore.YELLOW)

    dst_string = return_pretty_print_string(str(file["dst"]), str(file["dst"].name), start="", color=Fore.CYAN)

    ext_path = extensions[file["src"].suffix].split("\\")[-1]
    dst_string = return_pretty_print_string(dst_string, file["src"].suffix, start="", color=Fore.YELLOW)

    pretty_print_substring(dst_string, ext_path, start="\u2794    To:  ", end='\n', color=Fore.YELLOW)


if __name__ == "__main__":
    main()
