#!/usr/bin/env python

import logging

from tkinter import messagebox
from os import path, mkdir
from frontend import App
from backend.configs import CONFIGS, create_config_file, read_config


if __name__ == "__main__":
    # read configurations
    try:
        if not path.exists(path.abspath("CONFIG.ini")):
            create_config_file()

        read_config()
    except Exception as e:
        messagebox.showerror(
            "Error reading CONFIG.ini file",
            f"An error occurred reading the configuration file. Detail: {e}",
        )
        exit(1)

    # set up logging
    if not path.exists(path.abspath(CONFIGS["APP"]["log_dir"])):
        mkdir(path.abspath(CONFIGS["APP"]["log_dir"]))

    logging.basicConfig(
        filename=path.join(path.abspath(CONFIGS["APP"]["log_dir"]), "app.log"),
        format="[%(asctime)s]:%(levelname)s:%(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        encoding="utf-8",
        level=logging.WARNING,
    )

    logging.info("Application initialized")

    app = App()
    app.run()

    logging.info("Application terminated")
