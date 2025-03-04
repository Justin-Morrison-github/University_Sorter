import json
from pathlib import Path


class Settings():
    JSON_FILE = "json_file"

    BASEPATH = "basepath"
    SRC_PATH = "src_path"
    DST_PATH = "dst_path"

    def __init__(self, settings_file, current_file):
        with open(settings_file, 'r') as settings_json:
            settings: dict = json.load(settings_json)[current_file]

        self.basepath = Path(settings.get(Settings.BASEPATH, "NULL"))
        self.src_path = Path(settings.get(Settings.SRC_PATH, "NULL"))
        self.dst_path = Path(settings.get(Settings.DST_PATH, "NULL"))

        if not self.basepath.exists() and self.basepath.name != "NULL":
            raise FileNotFoundError(self.basepath)
        if not self.src_path.exists() and self.src_path.name != "NULL":
            raise FileNotFoundError(self.src_path)
        if not self.dst_path.exists() and self.dst_path.name != "NULL":
            raise FileNotFoundError(self.dst_path)

        self.json_file = Path(settings.get(Settings.JSON_FILE, "NULL"))
        if not self.json_file.exists() and self.json_file.name != "NULL":
            raise FileNotFoundError(self.json_file)
