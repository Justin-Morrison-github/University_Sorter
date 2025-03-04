
import pytest
from colorama import Fore, init as colorama_init
import sys
from pathlib import Path
import os

curr_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(curr_dir)

from university import Packet, Folder, Settings

@pytest.fixture
def settings():
    return Settings("app/json/settings.json", "university")


def test_Settings(settings: Settings):
    assert settings.dst_path == Path("C:/Users/morri/Onedrive/University")
    assert settings.src_path == Path("C:/Users/morri/Downloads")
    assert settings.json_file == Path("app/json/courses.json")


@pytest.fixture
def packet(settings: Settings):
    src = Path(f"{settings.src_path}/CHEM 1101 Assignment 1")
    dst = Path(f"{settings.dst_path}/02_Second-Year Classes/FALL/Chemistry/CHEM 1101 Assignment 1")
    course_code = "CHEM1101"
    name = "Chemistry"
    packet = Packet(src, dst, course_code, name, Folder.ASSIGNMENT)
    return packet


def test_Packet_default_init():
    with pytest.raises(TypeError):
        packet = Packet()


def test_Packet_init(packet: Packet):
    assert packet.src == Path("C:/Users/morri/Downloads/CHEM 1101 Assignment 1")
    assert packet.dst == Path(
        "C:/Users/morri/OneDrive/University/02_Second-Year Classes/FALL/Chemistry/CHEM 1101 Assignment 1")
    assert packet.course_code == "CHEM1101"
    assert packet.course_name == "Chemistry"
    assert packet.folder_type == Folder.ASSIGNMENT
    assert packet.error == None
