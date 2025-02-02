from enum import StrEnum


class ANSI(StrEnum):
    ARROW = "⮡ "
    STRAIGHT_ARROW = "➔ "
    SUCCESS = "☑ "
    FAILURE = "☒ "
    WARNING = "⚠ "
    INDENT = "    "
    B_FAILURE = "❌ "
    B_SUCCESS = "✅ "
