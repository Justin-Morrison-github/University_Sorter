from enum import StrEnum
from colorama import Fore


class Style(StrEnum):
    # ANSI escape Sequences
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

    # Special Characters/Symbols
    ARROW = "⮡ "
    STRAIGHT_ARROW = "➔ "
    SUCCESS_CHAR = "☑ "
    FAILURE_CHAR = "☒ "
    WARNING_CHAR = "⚠ "
    INDENT = "    "
    B_FAILURE = "❌ "
    B_SUCCESS = "✅ "

    # Colors with symbols
    SUCCESS = f"{Fore.GREEN}{SUCCESS_CHAR}"
    WARNING = f"{Fore.YELLOW}{WARNING_CHAR}"
    FAILURE = f"{Fore.RED}{FAILURE_CHAR}"

    SUCCESS_ARROW = f"{Fore.GREEN}{ARROW}"
    WARNING_ARROW = f"{Fore.YELLOW}{ARROW}"
    FAILURE_ARROW = f"{Fore.RED}{ARROW}"

    # Symbols with colors and indents
    TAB_ARROW = f"{INDENT}{ARROW}"
    TAB_SUCCESS = f'{INDENT}{SUCCESS}'
    TAB_FAILURE = f'{INDENT}{FAILURE}'
    TAB_WARNING = f'{INDENT}{WARNING}'

    TAB_YELLOW_ARROW = f'{INDENT}{WARNING_ARROW}'
