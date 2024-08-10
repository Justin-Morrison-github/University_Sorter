import os
from move import send_file, user_continues


def main():
    basepath = "C:\\Users\\morri\\OneDrive\\University"

    university = {
        "01_First-Year Classes": {
            "FALL": ["MATH1004", "CHEM1101", "ECOR1048", "ECOR1055", "ECOR1057", "ECOR1046", "ECOR1045", "PHYS1003", "ECOR1047"],
            "WINTER": ["ECOR1043", "ECOR1042", "PHYS1004", "ECOR1056", "GEOG1020", "MATH1104", "ECOR1044", "ECOR1041"],
        },
        "02_Second-Year Classes": {
            "FALL": ["ELEC2501", "COOP1000", "MATH1005", "SYSC2310", "COMP1805", "SYSC2006"],
            "WINTER": ["SYSC2100", "CCDP2100", "SYSC2320", "COMP2804", "SYSC2004"],
        }
    }

    classes = {}

    for year, semesters in university.items():
        for semester, class_list in semesters.items():
            folder_path = os.path.join(basepath, year, semester)
            class_paths = get_class_paths(folder_path)
            classes.update(dict(zip(class_list, class_paths)))

    src_folder_path = "C:\\Users\\morri\\Downloads"
    files_to_be_sent = traverse_folder(src_folder_path, classes)

    if len(files_to_be_sent) == 0:
        print("No files were found")
    else:
        for file in files_to_be_sent:
            print(f'\u2794  From:   {file["src"]}')
            print(f'\u2794    To:   {file["dst"]}\n')

        if user_continues():
            for file in files_to_be_sent:
                send_file(file["src"], file["dst"])


def get_class_paths(folder_path):
    classes = []
    for folder in os.listdir(folder_path):
        if (os.path.isdir(os.path.join(folder_path, folder))):
            classes.append(os.path.join(folder_path, folder))

    return classes


def traverse_folder(src_folder_path: str, class_folders: dict) -> list[dict]:
    files_to_be_sent = []

    for root, _, files in os.walk(src_folder_path):
        for file in files:
            filename, _ = os.path.splitext(file)
            # Only works if files have specific filenames, example: ELEC 2501.txt
            classname = filename[:4] + filename[5:9]

            if classname in class_folders:
                files_to_be_sent.append(
                    {
                        "src": os.path.join(root, file),
                        "dst": os.path.join(class_folders[classname], file)
                    }
                )

    return files_to_be_sent


if __name__ == "__main__":
    main()
