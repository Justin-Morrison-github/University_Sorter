import os
import sys
import unittest

# Adjusting path for imports
curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(curr_dir)

from university import Packet, Folder, Settings
from colorama import init as colorama_init
from pathlib import Path


class TestSettings(unittest.TestCase):
    def setUp(self):
        self.settings = Settings("app/json/settings.json", "university")

    def test_Settings_init(self):
        self.assertEqual(self.settings.dst_path, Path("C:/Users/morri/Onedrive/University"))
        self.assertEqual(self.settings.src_path, Path("C:/Users/morri/Downloads"))
        self.assertEqual(self.settings.basepath, Path("NULL")) # Not being used
        self.assertEqual(self.settings.json_file, Path("app/json/courses.json"))

    def test_Settings_init_invalid_path(self):
        with self.assertRaises(FileNotFoundError) as context:
            settings = Settings("settings.json", "university"), FileNotFoundError


class TestPacket(unittest.TestCase):
    def setUp(self):
        self.settings = Settings("app/json/settings.json", "university")
        self.src = Path(f"{self.settings.src_path}/CHEM 1101 Assignment 1")
        self.dst = Path(f"{self.settings.dst_path}/02_Second-Year Classes/FALL/Chemistry/CHEM 1101 Assignment 1")
        self.course_code = "CHEM1101"
        self.name = "Chemistry"
        self.packet = Packet(self.src, self.dst, self.course_code, self.name, Folder.ASSIGNMENT)

    def test_Packet_default_init(self):
        with self.assertRaises(TypeError):
            Packet()

    def test_Packet_init(self):
        self.assertEqual(self.packet.src, Path("C:/Users/morri/Downloads/CHEM 1101 Assignment 1"))
        self.assertEqual(self.packet.dst, Path(
            "C:/Users/morri/OneDrive/University/02_Second-Year Classes/FALL/Chemistry/CHEM 1101 Assignment 1"))
        self.assertEqual(self.packet.course_code, "CHEM1101")
        self.assertEqual(self.packet.course_name, "Chemistry")
        self.assertEqual(self.packet.folder_type, Folder.ASSIGNMENT)
        self.assertIsNone(self.packet.error)


if __name__ == "__main__":
    unittest.main()
