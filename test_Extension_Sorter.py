import unittest
from pathlib import Path
import tempfile
from ExtensionSorter import get_files_to_be_sent, get_pretty_dst_string, get_pretty_src_string
from colorama import Fore
from Settings import Settings
from ANSI import ANSI
import json


class TestExtensionSorter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.settings = Settings("JSON/settings.json", "ExtensionSorter")

    def test_settings(self):
        if Path.cwd().anchor == '/':
            self.assertEqual(self.settings.src_path, Path("/mnt/c/Users/morri/Downloads"))
        else:
            self.assertEqual(self.settings.src_path, Path("C:/Users/morri/Downloads"))

        self.assertEqual(self.settings.json_file, Path("JSON/extensions.json"))
        self.assertTrue(self.settings.json_file.exists())
        self.assertTrue(self.settings.src_path.exists())

    def setUp(self):
        with open(self.settings.json_file) as json_file:
            self.extensions = json.load(json_file)
        self.expected_keys = {"AUDIO", "CODE", "FOLDERS", "IMAGES", "INSTALLERS", "OTHER", "TEXT"}

    def test_missing_keys(self):
        # Ensure all expected keys are present in the JSON
        for key in self.expected_keys:
            self.assertIn(key, self.extensions, f"Missing expected key: {key}")

    def test_unexpected_keys(self):
        # Ensure no extra keys are present in the JSON
        actual_keys = set(self.extensions.keys())
        unexpected_keys = actual_keys - self.expected_keys
        self.assertFalse(
            unexpected_keys, f"Unexpected keys found: {', '.join(unexpected_keys)}"
        )

    def test_values_are_strings(self):
        # Ensure all values in the JSON are strings
        for category, items in self.extensions.items():
            for extension, value in items.items():
                self.assertIsInstance(
                    value, str,
                    f"Value for '{extension}' in category '{category}' is not a string: {value}"
                )

    def test_file_extension_format(self):
        # Ensure all keys (file extensions) start with a dot, except specific allowed cases
        allowed_empty_key_categories = {"FOLDERS"}  # e.g., FOLDERS allows empty string as a key
        for category, items in self.extensions.items():
            for extension in items.keys():
                if category in allowed_empty_key_categories and extension == "":
                    continue  # Skip the allowed empty key case
                self.assertTrue(
                    extension.startswith("."),
                    f"Key '{extension}' in category '{category}' does not start with a dot"
                )

    def test_case_sensitivity_of_keys(self):
        # Check case sensitivity for keys in the JSON
        for category, items in self.extensions.items():
            for key in items.keys():
                # Try accessing the key with altered case
                upper_key = key.upper()
                lower_key = key.lower()
                if key not in {upper_key, lower_key}:
                    self.assertNotIn(
                        upper_key, items,
                        f"Case sensitivity failed: found uppercase version '{upper_key}' of key '{key}'"
                    )
                    self.assertNotIn(
                        lower_key, items,
                        f"Case sensitivity failed: found lowercase version '{lower_key}' of key '{key}'"
                    )

    def test_for_duplicate_keys(self):
        for category, items in self.extensions.items():
            keys = list(items.keys())
            unique_keys = set(keys)
            self.assertEqual(
                len(keys), len(unique_keys),
                f"Duplicate keys found in category '{category}'"
            )

    def test_audio(self):
        self.assertEqual(len(self.extensions["AUDIO"]), 2)
        self.assertEqual(self.extensions["AUDIO"][".mp3"], "AUDIO/MP3")
        self.assertEqual(self.extensions["AUDIO"][".wav"], "AUDIO/WAV")

    def test_code(self):
        self.assertEqual(len(self.extensions["CODE"]), 4)
        self.assertEqual(self.extensions["CODE"][".py"], "CODE/PYTHON")
        self.assertEqual(self.extensions["CODE"][".cs"], "CODE/C#")
        self.assertEqual(self.extensions["CODE"][".c"], "CODE/C")
        self.assertEqual(self.extensions["CODE"][".java"], "CODE/JAVA")

    def test_folders(self):
        self.assertEqual(len(self.extensions["FOLDERS"]), 2)
        self.assertEqual(self.extensions["FOLDERS"][".zip"], "FOLDERS/ZIP")
        self.assertEqual(self.extensions["FOLDERS"][""], "FOLDERS/Folders")

    def test_images(self):
        self.assertEqual(len(self.extensions["IMAGES"]), 5)
        self.assertEqual(self.extensions["IMAGES"][".pdf"], "IMAGES/PDF")
        self.assertEqual(self.extensions["IMAGES"][".png"], "IMAGES/PNG")
        self.assertEqual(self.extensions["IMAGES"][".jpg"], "IMAGES/JPG")
        self.assertEqual(self.extensions["IMAGES"][".ico"], "IMAGES/ICON")
        self.assertEqual(self.extensions["IMAGES"][".HEIC"], "IMAGES/HEIC")

    def test_installers(self):
        self.assertEqual(len(self.extensions["INSTALLERS"]), 2)
        self.assertEqual(self.extensions["INSTALLERS"][".exe"], "INSTALLERS/EXE")
        self.assertEqual(self.extensions["INSTALLERS"][".msi"], "INSTALLERS/MSI")

    def test_other(self):
        self.assertEqual(len(self.extensions["OTHER"]), 5)
        self.assertEqual(self.extensions["OTHER"][".f3d"], "OTHER/FUSION")
        self.assertEqual(self.extensions["OTHER"][".otf"], "OTHER/FONTS")
        self.assertEqual(self.extensions["OTHER"][".metadata"], "OTHER/METADATA")
        self.assertEqual(self.extensions["OTHER"][".tracktionedit"], "OTHER/TRACKTION")
        self.assertEqual(self.extensions["OTHER"][".vsix"], "OTHER/VSIX")

    def test_text(self):
        self.assertEqual(len(self.extensions["TEXT"]), 5)
        self.assertEqual(self.extensions["TEXT"][".txt"], "TEXT/TXT")
        self.assertEqual(self.extensions["TEXT"][".docx"], "TEXT/WORD")
        self.assertEqual(self.extensions["TEXT"][".xlsx"], "TEXT/EXCEL")
        self.assertEqual(self.extensions["TEXT"][".ppt"], "TEXT/POWERPOINT")
        self.assertEqual(self.extensions["TEXT"][".pptx"], "TEXT/POWERPOINT")

    def test_top_level_keys(self):
        # Test the total number of categories
        self.assertEqual(len(self.extensions), 7)

    def test_get_files_to_be_sent_with_tempfile(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            src_file_1 = root / "test.mp3"
            src_file_2 = root / "test.wav"

            audio = root / "AUDIO"
            mp3 = audio / "MP3"
            wav = audio / "WAV"
            dst_file_1 = mp3 / "test.mp3"
            dst_file_2 = wav / "test.wav"

            # Create source file
            src_file_1.write_text("Mock file 1.")
            src_file_2.write_text("Mock file 2.")

            expected_file_to_be_sent = [{
                "src": src_file_1,
                "dst": dst_file_1
            }, {
                "src": src_file_2,
                "dst": dst_file_2
            }]

            files_to_be_sent = get_files_to_be_sent(self.extensions, root)

            for file in files_to_be_sent:
                self.assertIn(file, expected_file_to_be_sent)

            self.assertEqual(files_to_be_sent, expected_file_to_be_sent)

    def test_get_pretty_src_string(self):
        test_src = {"src": Path("C:/Users/morri/Downloads/Untitled.png")}

        actual_string = get_pretty_src_string(test_src)
        expected_string = f"{ANSI.ARROW} From: C:/Users/morri/Downloads/{Fore.CYAN}Untitled{Fore.YELLOW}.png{Fore.RESET}{Fore.RESET}"
        self.assertEqual(actual_string, expected_string)

    def test_get_pretty_src_stringV2(self):
        test_dst = {"dst": Path("C:/Users/morri/Downloads/IMAGES/PNG/Untitled.png")}

        actual_string = get_pretty_dst_string(test_dst)
        expected_string = f"{ANSI.ARROW}   To: C:/Users/morri/Downloads/IMAGES/{Fore.YELLOW}PNG{Fore.RESET}/{Fore.CYAN}Untitled.png{Fore.RESET}"
        self.assertEqual(actual_string, expected_string)


if __name__ == "__main__":
    unittest.main(verbosity=0)
