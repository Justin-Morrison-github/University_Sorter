# import os
from pathlib import Path
from move import send_file, user_continues


def main():

    destination = Path("C:\\Users\\morri\\OneDrive\\Music\\Songs")
    src_folder = Path("C:\\Users\\morri\\Downloads\\AUDIO\\MP3")
    files_to_be_sent = []

    for file in src_folder.iterdir():
        if file.suffix == ".mp3":
            files_to_be_sent.append(
                {
                    "src": src_folder / file.name,
                    "dst": destination / file.name
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
