import json
from pathlib import Path

class Settings():
    JSON_FILE = "json_file"
    
    WIN_BASEPATH = "win_basepath"
    WIN_SRC_PATH = "win_src_path"
    WIN_DST_PATH = "win_dst_path"

    WSL_BASEPATH = "wsl_basepath"
    WSL_SRC_PATH = "wsl_src_path"
    WSL_DST_PATH = "wsl_dst_path"

    PATHS_TO_CHECK = "paths_to_check"

    def __init__(self, settings_file, current_file):
        with open(settings_file, 'r') as settings_json:
            settings: dict = json.load(settings_json)[current_file]
        
        if Path.cwd().anchor == '/':
            self.basepath = Path(settings.get(Settings.WSL_BASEPATH, "NULL"))
            self.src_path = Path(settings.get(Settings.WSL_SRC_PATH, "NULL"))
            self.dst_path = Path(settings.get(Settings.WSL_DST_PATH, "NULL"))

        else:
            self.basepath = Path(settings.get(Settings.WIN_BASEPATH, "NULL"))
            self.src_path = Path(settings.get(Settings.WIN_SRC_PATH, "NULL"))
            self.dst_path = Path(settings.get(Settings.WIN_DST_PATH, "NULL"))

        self.json_file = Path(settings.get(Settings.JSON_FILE, "NULL"))
        self.paths_to_check = settings.get(Settings.PATHS_TO_CHECK, "NULL")
        self.root = "NULL"
