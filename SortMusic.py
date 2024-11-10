import json
from pathlib import Path
from move import send_file, user_continues
from Settings import Settings

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
            print(f'\u2794  From:   {file["src"]}')
            print(f'\u2794    To:   {file["dst"]}\n')

        if user_continues():
            for file in files_to_be_sent:
                send_file(file["src"], file["dst"])


if __name__ == "__main__":
    main()
