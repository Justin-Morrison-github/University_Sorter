from enum import StrEnum, auto


class Settings(StrEnum):
    JSON_FILE = auto()
    WIN_BASEPATH = auto()
    WSL_BASEPATH = auto()
    WIN_SRC_PATH = auto()
    WSL_SRC_PATH = auto()
