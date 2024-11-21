import unittest
from pathlib import Path
import tempfile
from ExtensionSorter import get_files_to_be_sent
from colorama import Fore
from Settings import Settings

class TestExtensionSorter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.extensions = {
            "AUDIO": {
                ".mp3": "AUDIO/MP3",  # Use forward slashes for cross-platform paths
                ".wav": "AUDIO/WAV"
            },
        }
    
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

            self.assertEqual(files_to_be_sent, expected_file_to_be_sent)
            self.assertEqual(files_to_be_sent, expected_file_to_be_sent)

            # # Check if the file was moved (optional: if the function moves files)
            # self.assertTrue(dst_file_path.exists())
            # self.assertFalse(src_file_path.exists())  # Ensure the source file no longer exists

    def test_set_up_settings(self):
        actual_settings = Settings("JSON/settings.json", "ExtensionSorter")

        self.assertEqual(actual_settings.json_file, Path("JSON/extensions.json"))
        self.assertEqual(actual_settings.win_src_path, Path("C:/Users/morri/Downloads"))
        self.assertEqual(actual_settings.wsl_src_path, Path("/mnt/c/Users/morri/Downloads"))
       
if __name__ == "__main__":
    unittest.main()
