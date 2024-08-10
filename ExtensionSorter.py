import os
from move import send_file, user_continues


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
            _, ext = os.path.splitext(file)

            if ext in extensions:
                files_to_be_sent.append(
                    {
                        "src": os.path.join(sourceFolder, file),
                        "dst": os.path.join(sourceFolder, extensions[ext], file)
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
