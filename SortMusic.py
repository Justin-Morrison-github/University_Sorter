import os
from move import send_file, user_continues


def main():

    DESTINATION = "C:\\Users\\morri\\OneDrive\\Music\\Songs"
    SOURCE_FOLDER = "C:\\Users\\morri\\Downloads\\AUDIO\\MP3"
    files_to_be_sent = []

    for file in os.listdir(SOURCE_FOLDER):
        if file.endswith(".mp3"):
            files_to_be_sent.append(
                {
                    "src": os.path.join(SOURCE_FOLDER, file),
                    "dst": os.path.join(DESTINATION, file)
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
