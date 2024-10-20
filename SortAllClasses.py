from pathlib import Path
from enum import StrEnum, auto, Enum


class Course(StrEnum):
    ASSIGNMENTS = "Assignments"
    CODE = "Code"
    INFO = "Course Information"
    LABS = "Labs"
    LECTURE = "Lectures"
    PASS = "Pass"
    PRACTICE = "Practice"
    REVIEW = "Review"
    TEXTBOOK = "Textbook"
    TUTORIAl = "Tutorial"
    WOOCLAP = "Wooclap"

    ELEC2501 = "Circuits and Signals"
    MATH1005 = "Differential Equations"
    SYSC2310 = "Digital Systems"
    COMP1805 = "Discrete Structures I"
    SYSC2006 = "Imperative Programming"


class Tag(Enum):
    ASSIGNMENT = "Assignments"
    INFO = "Course Information"
    LAB = "Labs"
    LECTURE = "Lectures"
    REVIEW = "Review"
    PASS = "Pass"
    TEXTBOOK = "Textbook"
    TUTURIAL = "Tutorial"
    WOOCLAP = "Wooclap"
    CODE = "Code"
    PRACTICE = "Practice"


def main():
    basepath = "C:\\Users\\morri\\OneDrive\\University\\02_Second-Year Classes\\FALL"
    root = Path(basepath)
    if not root.exists():
        print('Error')
        exit()

    classes = {Course.ELEC2501: [Course.ASSIGNMENTS, Course.INFO, Course.LABS,
                                 Course.LECTURE, Course.REVIEW, Course.PASS, Course.TEXTBOOK, Course.TUTORIAl],
               Course.MATH1005: [Course.INFO, Course.LECTURE, Course.REVIEW, Course.PRACTICE, Course.TEXTBOOK, Course.TUTORIAl],
               Course.SYSC2310: [Course.ASSIGNMENTS, Course.PRACTICE, Course.INFO, Course.LABS,
                                 Course.LECTURE, Course.REVIEW, Course.PRACTICE, Course.TEXTBOOK, Course.WOOCLAP],
               Course.COMP1805: [Course.ASSIGNMENTS, Course.INFO,
                                 Course.LECTURE, Course.REVIEW, Course.PASS, Course.PRACTICE, Course.TEXTBOOK, Course.TUTORIAl],
               Course.SYSC2006: [Course.ASSIGNMENTS, Course.CODE, Course.INFO, Course.LABS,
                                 Course.LECTURE, Course.REVIEW, Course.PASS, Course.PRACTICE, Course.TEXTBOOK, Course.WOOCLAP]
               }

    setup_folders(root, classes)
    organize_files(root, classes)


def organize_files(root: Path, classes: dict):
    for course, folders in classes.items():
        class_path = root / course
        if not class_path.exists():
            print("Error")
            exit()

        print(f"{course.name}:")
        for folder in folders:
            print(f"\t/{folder}:")

            matching_files = list(class_path.glob(f"* {Tag(folder).name} *"))
            if matching_files:
                dest_folder = class_path / folder
                for file in matching_files:
                    print(f"\t{file.name}")
                    dest = dest_folder / file.name
                    file.rename(dest)
            else:
                print("\t\tNo Files Sent")


def setup_folders(root: Path, classes: dict):
    for course in root.iterdir():
        if course.name in classes:
            class_path = root / course
            for folder in classes[course.name]:
                dir = Path(class_path / folder)
                if not dir.exists():
                    print(f"Making {dir.name}")
                    dir.mkdir()


if __name__ == "__main__":
    main()
