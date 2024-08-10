import os
from sys import argv
from move import prompt_user


def main():
    # init_dir = "C:\\Users\\morri\\Downloads"
    search_folders = ["C:\\Users\\morri\\Downloads", "C:\\Users\\morri\\Onedrive",
                      "C:\\Users\\morri\\OneDrive - Carleton University", "C:\\Users\\morri\\Documents"]

    if len(argv) == 1:  # No folder given
        folder = prompt_user("Enter Folder Name: ")
        find_folder_path_from_name(folder, search_folders)
    elif len(argv) == 2:  # Folder given
        find_folder_path_from_name(argv[1], search_folders)


def find_folder_path_from_name(folder_name, folders_to_search):
    path = ""
    count = 0
    found_folders = []
    for folder in folders_to_search:
        for dirpath, dirnames, _ in os.walk(folder):
            for dir in dirnames:
                count += 1
                print(count)
                if dir.lower() == folder_name.lower():
                    path = os.path.join(dirpath, dir)
                    found_folders.append(path)

    for folder in found_folders:
        print(folder)

    if len(found_folders) > 1:
        return found_folders
    elif len(found_folders) == 1:
        return found_folders[0]
    else:
        print("Folder Not Found")
        return None


if __name__ == '__main__':
    main()
