from app import university
from pathlib import Path
from colorama import Fore, init as colorama_init
from src.Settings import Settings

import pytest


@pytest.fixture
def settings():
    return Settings("json/settings.json", "university")


def test_Settings(settings: Settings):
    assert settings.dst_path == Path("C:/Users/morri/Onedrive/University")
    assert settings.src_path == Path("C:/Users/morri/Downloads")
    assert settings.json_file == Path("json/courses.json")


@pytest.fixture
def packet(settings: Settings):
    src = Path(f"{settings.src_path}/CHEM 1101 Assignment 1")
    dst = Path(f"{settings.dst_path}/02_Second-Year Classes/FALL/Chemistry/CHEM 1101 Assignment 1")
    course_code = "CHEM1101"
    name = "Chemistry"
    packet = university.Packet(src, dst, course_code, name, university.Folder.ASSIGNMENT)
    return packet


def test_Packet_default_init():
    with pytest.raises(TypeError):
        packet = university.Packet()


def test_Packet_init(packet: university.Packet):
    assert packet.src == Path("C:/Users/morri/Downloads/CHEM 1101 Assignment 1")
    assert packet.dst == Path(
        "C:/Users/morri/OneDrive/University/02_Second-Year Classes/FALL/Chemistry/CHEM 1101 Assignment 1")
    assert packet.course_code == "CHEM1101"
    assert packet.course_name == "Chemistry"
    assert packet.folder_type == university.Folder.ASSIGNMENT
    assert packet.error == None
