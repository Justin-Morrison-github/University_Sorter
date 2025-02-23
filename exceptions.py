from colorama import Fore
from Style import Style
from pathlib import Path
from string_utils import underline, underline_color, pretty_substring



class PathException(Exception):
    def __init__(self, path, type: 'PathException', msg=""):
        self.path: Path = path
        self.type: PathException = type
        self.msg: str = msg
        super().__init__(self.msg)

    def __str__(self):
        return f"{Style.TAB_WARNING}({self.type}): {self.msg}"


class FolderNotEmpty(PathException):
    def __init__(self, folder: Path):
        self.folder: Path = folder
        self.msg: str = f"{underline_color(folder)} Folder Not Empty (Could Not Delete)"
        super().__init__(self.folder, __class__.__name__, self.msg)

    def __str__(self):
        return super().__str__()


class SourcePathDoesNotExist(PathException):
    def __init__(self, path: Path):
        self.path: Path = path
        self.msg: str = f"{underline_color(path)} Source Path Does Not Exist"
        super().__init__(self.path, __class__.__name__, self.msg)

    def __str__(self):
        return super().__str__()


class DestinationPathAlreadyExists(PathException):
    def __init__(self, path: Path):
        self.path = path
        file_and_parent = f"{self.path.parent.name}\\{self.path.name}"
        self.msg = f"{pretty_substring(str(self.path), file_and_parent)}"
        super().__init__(self.path, __class__.__name__, self.msg)

    def __str__(self):
        return super().__str__()


class DestinationParentDoesNotExist(PathException):
    def __init__(self, path: Path):
        self.path = path
        self.msg = f"{Fore.CYAN}{underline(self.path.parent.name)}{Fore.CYAN} Parent Folder Does Not Exist"
        super().__init__(self.path, __class__.__name__, self.msg)

    def __str__(self):
        return super().__str__()

if __name__ == "__main__":
    path = Path("one/two/three")
    err = DestinationPathAlreadyExists(path)
    print(err)