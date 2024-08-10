import os
from move import pretty_print_substring, pretty_path


def main():
    basepath = "C:\\Users\\morri\\Downloads"
    word = prompt_user_for_input()
    files = get_files_containing_word(basepath, word)
    for file in files:
        pretty_path(file, basepath)
        # pretty_print_substring(file["src"], word)


def prompt_user_for_input() -> str:
    while True:
        check = input("Enter common word in file name: ")

        if check.lower() == 'q':
            print("Quit Program")
            exit()
        else:
            print()
            return check


def get_files_containing_word(folder_path: str, word: str):
    file_list = []

    for dirpath, _, filenames in os.walk(folder_path):
        for file in filenames:
            if word.lower() in file.lower():
                file_list.append(
                    {
                        "src": os.path.join(dirpath, file),
                    }
                )

    return file_list


if __name__ == '__main__':
    main()
