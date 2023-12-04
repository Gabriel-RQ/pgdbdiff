"""
This module reads the configuration file and offers utilities to modify it.
"""

import shutil
import configparser
from os import path


CONFIGS = configparser.ConfigParser()


def read_config() -> None:
    CONFIGS.read("CONFIG.ini")


def create_config_file(cfg_path: str = ".") -> None:
    open(path.join(cfg_path, "CONFIG.ini"), "w").close()  # creates the config file
    shutil.copy(
        src=path.join(cfg_path, "CONFIG.ini.example"),
        dst=path.join(cfg_path, "CONFIG.ini"),
    )


def save_config() -> None:
    CONFIGS["RUNNING"]["first_db"] = ""
    CONFIGS["RUNNING"]["second_db"] = ""

    with open("CONFIG.ini", "w") as config_file:
        CONFIGS.write(config_file)
