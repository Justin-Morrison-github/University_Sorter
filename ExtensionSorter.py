import os
from move import send_file, user_continues, pretty_print_substring, return_pretty_print_string
from colorama import Fore


def main():
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

    sourceFolder = "C:\\Users\\morri\\Downloads"
    files_to_be_sent = []

    for file in os.listdir(sourceFolder):
        if not os.path.isdir(os.path.join(sourceFolder, file)):
            name, ext = os.path.splitext(file)

            if ext in extensions:
                files_to_be_sent.append(
                    {
                        "src": os.path.join(sourceFolder, file),
                        "dst": os.path.join(sourceFolder, extensions[ext], file),
                        "ext": ext,
                        "name": name
                    }
                )

    if len(files_to_be_sent) == 0:
        print("No files were found")
    else:
        for file in files_to_be_sent:
            print_file(file, extensions)

        if user_continues():
            for file in files_to_be_sent:
                send_file(file["src"], file["dst"])


def print_file(file: dict, extensions: dict):
    src_string = return_pretty_print_string(file["src"], file["name"], start="", color=Fore.CYAN)
    pretty_print_substring(src_string, file["ext"], start="\u2794  From:  ", color=Fore.YELLOW)

    dst_string = return_pretty_print_string(file["dst"], file["name"], start="", color=Fore.CYAN)

    ext_path = extensions[file["ext"]].split("\\")[-1]
    dst_string = return_pretty_print_string(dst_string, file["ext"], start="", color=Fore.YELLOW)

    pretty_print_substring(dst_string, ext_path, start="\u2794    To:  ", end='\n', color=Fore.YELLOW)


if __name__ == "__main__":
    main()
