import os
import sys
import unittest

# Adjusting path for imports
curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(curr_dir)

from string_utils import path_from_substring, pretty_substring, underline, color, underline_color
from colorama import init as colorama_init, Fore
from pathlib import Path
from Style import Style


class TestStringUtils(unittest.TestCase):
    def setUp(self):
        self.str = "This is a string"
        self.substr1 = "This"
        self.substr2= "is a"
        self.substr3 = "string"


        self.str_longpath = "a/b/c/test.txt"
        self.filepath = "test.txt"

        self.longpath = Path(self.str_longpath)
        self.file = Path(self.filepath)


    def test_underline(self):
        self.assertEqual(underline(self.str), f"{Style.UNDERLINE}This is a string{Style.RESET}")
        self.assertEqual(underline(self.substr1), f"{Style.UNDERLINE}This{Style.RESET}")

    def test_color(self):
        self.assertEqual(color(self.str, Fore.YELLOW), f"{Fore.YELLOW}This is a string{Fore.RESET}")
        self.assertEqual(color(self.substr1, Fore.RED), f"{Fore.RED}This{Fore.RESET}")
    
    def test_underline_color(self):
        #Default color
        self.assertEqual(underline_color(self.str), f"{Style.UNDERLINE}{Fore.YELLOW}This is a string{Style.RESET}")

        #Given color
        self.assertEqual(underline_color(self.substr1, Fore.RED), f"{Style.UNDERLINE}{Fore.RED}This{Style.RESET}")

    def test_path_from_substring(self):
        self.assertEqual(path_from_substring(self.longpath, self.filepath), Path("test.txt"))
        self.assertEqual(path_from_substring(self.longpath, self.filepath), self.file)

        self.assertEqual(path_from_substring(self.longpath, "c"), Path("c/test.txt"))
        
        self.assertEqual(path_from_substring(self.longpath, "b"), Path("b/c/test.txt"))

        self.assertEqual(path_from_substring(self.longpath, "a"), Path("a/b/c/test.txt"))

        #Test invalid case
        with self.assertRaises(ValueError) as context:
            path_from_substring(self.longpath, "abc"), Path("a/b/c/test.txt")

    def test_pretty_substring_default_args(self):
        # Default args
        self.assertEqual(
            pretty_substring(self.str, self.substr1), f"{Fore.YELLOW}This{Fore.RESET} is a string"
        )
        self.assertEqual(
            pretty_substring(self.str, self.substr2), f"This {Fore.YELLOW}is a{Fore.RESET} string"
        )
        self.assertEqual(
            pretty_substring(self.str, self.substr3), f"This is a {Fore.YELLOW}string{Fore.RESET}"
        )

    def test_pretty_substring(self):
        # Select start sequence
        self.assertEqual(
            pretty_substring(self.str, self.substr1, start="->"), f"->{Fore.YELLOW}This{Fore.RESET} is a string"
        )

        # Select end sequence
        self.assertEqual(
            pretty_substring(self.str, self.substr1, start="->", end = "\n"), f"->{Fore.YELLOW}This{Fore.RESET} is a string\n"
        )

        # Select color
        self.assertEqual(
            pretty_substring(self.str, self.substr1, color=Fore.RED), f"{Fore.RED}This{Fore.RESET} is a string"
        )



if __name__ == "__main__":
    unittest.main()
